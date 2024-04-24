import pygame
import random

# Constants
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 20
FRUIT_COUNT = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = "RIGHT"
        self.fruit_positions = []
        self.load_images()
        self.generate_fruits()
        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.game_over = False

    def load_images(self):
        self.snake_head_down_img = pygame.image.load("#Add Your file path for Snake head Image").convert_alpha()
        self.snake_body_img = pygame.image.load("Add Your file path for Snake Body image").convert_alpha()
        self.fruit_img = pygame.image.load("Add Your file path for Fruit/Points Image").convert_alpha()
        self.snake_head_down_img = pygame.transform.scale(self.snake_head_down_img, (TILE_SIZE, TILE_SIZE))
        self.snake_body_img = pygame.transform.scale(self.snake_body_img, (TILE_SIZE, TILE_SIZE))
        self.fruit_img = pygame.transform.scale(self.fruit_img, (TILE_SIZE, TILE_SIZE))

    def generate_fruits(self):
        for _ in range(FRUIT_COUNT):
            fruit_x = random.randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
            fruit_y = random.randint(0, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
            self.fruit_positions.append([fruit_x, fruit_y])

    def draw_snake(self):
        for i, segment in enumerate(self.snake):
            if i == 0:
                self.draw_rotated_head(segment)
            else:
                next_segment = self.snake[i - 1]
                self.draw_rotated_body(segment, next_segment)

    def draw_rotated_head(self, segment):
        if self.direction == "UP":
            rotated_image = pygame.transform.rotate(self.snake_head_down_img, 90)
        elif self.direction == "DOWN":
            rotated_image = pygame.transform.rotate(self.snake_head_down_img, -90)
        elif self.direction == "LEFT":
            rotated_image = pygame.transform.flip(self.snake_head_down_img, True, False)
        elif self.direction == "RIGHT":
            rotated_image = self.snake_head_down_img
        self.screen.blit(rotated_image, segment)

    def draw_rotated_body(self, segment, next_segment):
        dx = segment[0] - next_segment[0]
        dy = segment[1] - next_segment[1]
        if dx > 0:  # moving left
            rotated_image = pygame.transform.rotate(self.snake_body_img, 0)
        elif dx < 0:  # moving right
            rotated_image = pygame.transform.rotate(self.snake_body_img, 180)
        elif dy < 0:  # moving down
            rotated_image = pygame.transform.rotate(self.snake_body_img, 90)
        else:  # moving up
            rotated_image = pygame.transform.rotate(self.snake_body_img, -90)
        self.screen.blit(rotated_image, segment)

    def draw_fruits(self):
        for fruit in self.fruit_positions:
            self.screen.blit(self.fruit_img, (fruit[0], fruit[1]))

    def move_snake(self):
        head = self.snake[0].copy()
        if self.direction == "UP":
            head[1] -= TILE_SIZE
        elif self.direction == "DOWN":
            head[1] += TILE_SIZE
        elif self.direction == "LEFT":
            head[0] -= TILE_SIZE
        elif self.direction == "RIGHT":
            head[0] += TILE_SIZE

        self.snake.insert(0, head)

        for fruit in self.fruit_positions:
            if self.snake[0] == fruit:
                self.fruit_positions.remove(fruit)
                self.grow_snake()
                self.spawn_fruit()
                self.score += 1

        if (head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT or
                head in self.snake[1:]):
            self.game_over = True
            self.update_high_score()

        self.snake.pop()

    def grow_snake(self):
        tail = self.snake[-1].copy()
        self.snake.append(tail)

    def spawn_fruit(self):
        fruit_x = random.randint(0, WIDTH // TILE_SIZE - 1) * TILE_SIZE
        fruit_y = random.randint(0, HEIGHT // TILE_SIZE - 1) * TILE_SIZE
        self.fruit_positions.append([fruit_x, fruit_y])

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("high_score.txt", "w") as file:
                file.write(str(self.high_score))

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def display_high_score(self):
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, BLACK)
        self.screen.blit(high_score_text, (10, 50))

    def display_game_over(self):
        game_over_text = self.font.render("Game Over", True, BLACK)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        restart_text = self.font.render("Press SPACE to Restart", True, BLACK)
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height()))

    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
                    elif event.key == pygame.K_SPACE and self.game_over:
                        self.restart_game()

            if not self.game_over:
                self.move_snake()
                self.draw_snake()
                self.draw_fruits()
                self.display_score()
                self.display_high_score()
            else:
                self.display_game_over()

            pygame.display.flip()
            self.clock.tick(10)

    def restart_game(self):
        self.snake = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = "RIGHT"
        self.fruit_positions = []
        self.generate_fruits()
        self.score = 0
        self.game_over = False

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
