import pygame
import time
from Levels import get_levels 

pygame.init()

# Set up the screen
screen_width = 1000  # Increased width to accommodate score table and instructions
screen_height = 600
cell_size = 40  # Size of each cell in the maze
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game with Multiple Levels")

levels = get_levels()
current_level_index = 0
level_data = levels[current_level_index]

# Initialize scores for each level
scores = [[] for _ in levels]
combined_score_active = False
previous_score = 0

# Font for text rendering
font = pygame.font.Font(None, 36)

# Blob class definition
class Blob:
    def __init__(self, level_index):
        self.load_level(level_index)

    def load_level(self, level_index):
        level_data = levels[level_index]
        start_x, start_y = level_data["start"]
        self.x = (screen_width // 2 - len(level_data["maze"][0]) * cell_size // 2) + start_x * cell_size
        self.y = (screen_height // 2 - len(level_data["maze"]) * cell_size // 2) + start_y * cell_size
        self.size = cell_size
        self.color = (0, 255, 0)  # Green
        self.start_time = time.time()
        self.finished = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        if not self.finished:
            new_x = self.x + dx
            new_y = self.y + dy
            maze = levels[current_level_index]["maze"]
            cell_x = (new_x - (screen_width // 2 - len(maze[0]) * cell_size // 2)) // cell_size
            cell_y = (new_y - (screen_height // 2 - len(maze) * cell_size // 2)) // cell_size
            if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
                cell_type = maze[cell_y][cell_x]
                if cell_type == 0:
                    self.x = new_x
                    self.y = new_y
                elif cell_type == 3:
                    self.finish_level(new_x, new_y)
                elif cell_type == 9:
                    self.reset()
            else:
                self.reset()

    def finish_level(self, new_x, new_y):
        global previous_score, combined_score_active
        self.x = new_x
        self.y = new_y
        if not self.finished:
            elapsed_time = time.time() - self.start_time
            if combined_score_active and current_level_index == 1:
                total_time = previous_score + elapsed_time
                scores[current_level_index].append(total_time)
                scores[current_level_index].sort()
                if len(scores[current_level_index]) > 3:
                    scores[current_level_index].pop()
                print(f"Combined Level 1 & 2 completed in {total_time:.2f} seconds")
            else:
                scores[current_level_index].append(elapsed_time)
                scores[current_level_index].sort()
                if len(scores[current_level_index]) > 3:
                    scores[current_level_index].pop()
                print(f"Level {current_level_index + 1} completed in {elapsed_time:.2f} seconds")
            self.finished = True
            next_level()

    def reset(self):
        global combined_score_active, previous_score, current_level_index
        print("Blob has died! Resetting level...")
        current_level_index = 0  # Set current_level_index to 0 (maze 1)
        self.load_level(current_level_index)  # Load maze 1


def next_level():
    global current_level_index, blob, previous_score, combined_score_active
    if current_level_index == 0:
        previous_score = scores[current_level_index][0]
        combined_score_active = True
    elif current_level_index == 1:
        combined_score_active = False
    current_level_index = (current_level_index + 1) % len(levels)
    blob.load_level(current_level_index)

def draw_text():
    screen.fill((0, 0, 0), (0, 0, 200, screen_height))
    instructions = ["Controls:", "Move = Shift + Arrow", "R = Reset", "", "Top Times:"]
    y_offset = 120
    for text in instructions:
        instruction_text = font.render(text, True, (255, 255, 255))
        screen.blit(instruction_text, (30, y_offset))
        y_offset += 30
    
    # Display level 2 time
    y_offset += 20
    for score in scores[1][:3]:  # Display top 3 scores for level 2
        score_text = font.render(f"{score:.2f}s", True, (255, 255, 255))
        screen.blit(score_text, (50, y_offset))
        y_offset += 30



blob = Blob(current_level_index)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:
        blob.reset()

    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]):
        if not blob.finished:
            if keys[pygame.K_LEFT]:
                blob.move(-cell_size, 0)
            if keys[pygame.K_RIGHT]:
                blob.move(cell_size, 0)
            if keys[pygame.K_UP]:
                blob.move(0, -cell_size)
            if keys[pygame.K_DOWN]:
                blob.move(0, cell_size)

    screen.fill((0, 0, 0))
    maze = levels[current_level_index]["maze"]
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, ((screen_width // 2 - len(maze[0]) * cell_size // 2) + x * cell_size, (screen_height // 2 - len(maze) * cell_size // 2) + y * cell_size, cell_size, cell_size))
    blob.draw()
    draw_text()
    pygame.display.update()
