import pygame
import time
from Levels import get_levels

pygame.init()

# Setup
try:
    font = pygame.font.Font("assets/fonts/your_custom_font.ttf", 36)
except IOError:
    font = pygame.font.Font(None, 36)
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")

# Load levels
levels = get_levels()
scores = [[] for _ in levels]

class Blob:
    def __init__(self, level_index):
        self.level_index = level_index
        self.load_level(level_index)
    
    def load_level(self, level_index):
        self.level_data = levels[level_index]
        self.cell_size = min(screen_width // len(self.level_data["maze"][0]), screen_height // len(self.level_data["maze"]))
        start_x, start_y = self.level_data["start"]
        self.x = (screen_width // 2 - len(self.level_data["maze"][0]) * self.cell_size // 2) + start_x * self.cell_size
        self.y = (screen_height // 2 - len(self.level_data["maze"]) * self.cell_size // 2) + start_y * self.cell_size
        self.color = (0, 255, 0)
        self.start_time = time.time()
        self.finished = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.cell_size, self.cell_size))

    def move(self, dx, dy):
        if self.finished:
            return
        new_x = self.x + dx * self.cell_size
        new_y = self.y + dy * self.cell_size
        maze = self.level_data["maze"]
        cell_x = (new_x - (screen_width // 2 - len(maze[0]) * self.cell_size // 2)) // self.cell_size
        cell_y = (new_y - (screen_height // 2 - len(maze) * self.cell_size // 2)) // self.cell_size
        if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
            cell_type = maze[cell_y][cell_x]
            if cell_type == 0:
                self.x = new_x
                self.y = new_y
            elif cell_type == 3:
                self.finish_level()

    def finish_level(self):
        if not self.finished:
            elapsed_time = time.time() - self.start_time
            scores[self.level_index].append(elapsed_time)
            scores[self.level_index].sort()
            if len(scores[self.level_index]) > 3:
                scores[self.level_index] = scores[self.level_index][:3]
            print(f"Level {self.level_index + 1} completed in {elapsed_time:.2f} seconds")
            self.finished = True
            if self.level_index == len(levels) - 1:
                self.level_index = 0
                self.load_level(self.level_index)
            else:
                self.level_index += 1
                self.load_level(self.level_index)
            self.start_time = time.time()
            self.finished = False

def main_menu():
    menu_active = True
    while menu_active:
        screen.fill((0, 0, 0))
        title_text = font.render("Main Menu - High Scores", True, (255, 255, 255))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 50))
        for index, level_scores in enumerate(scores):
            score_texts = ", ".join(f"{score:.2f}s" for score in level_scores)
            text_surface = font.render(f"Level {index + 1} High Scores: {score_texts}", True, (255, 255, 255))
            screen.blit(text_surface, (50, 150 + index * 40))
        instruction_text = font.render("Press SPACE to Start or ESC to Exit", True, (255, 255, 255))
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, 500))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return 'start_game'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return 'quit'

def game_loop():
    blob = Blob(0)  # Start with the first level
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            blob.load_level(blob.level_index)  # Reset level
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if not blob.finished:
                if keys[pygame.K_LEFT]:
                    blob.move(-1, 0)
                elif keys[pygame.K_RIGHT]:
                    blob.move(1, 0)
                elif keys[pygame.K_UP]:
                    blob.move(0, -1)
                elif keys[pygame.K_DOWN]:
                    blob.move(0, 1)
        draw_maze(levels[blob.level_index]['maze'], blob)
        pygame.display.update()

def draw_maze(maze, blob):
    screen.fill((0, 0, 0))  # Clear the screen first
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, ((screen_width // 2 - len(maze[0]) * blob.cell_size // 2) + x * blob.cell_size, (screen_height // 2 - len(maze) * blob.cell_size // 2) + y * blob.cell_size, blob.cell_size, blob.cell_size))
    blob.draw()

# Main loop
action = 'main_menu'
while action != 'quit':
    if action == 'main_menu':
        action = main_menu()
    elif action == 'start_game':
        action = game_loop()


pygame.quit()
