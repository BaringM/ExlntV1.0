import pygame
import time

pygame.init()

# Set up the screen
screen_width = 1000  # Increased width to accommodate score table and instructions
screen_height = 600
cell_size = 40  # Size of each cell in the maze
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game with Multiple Levels")

# Define the mazes for each level
maze_level_1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Maze Level 2 as provided
maze_level_2 = [
    [1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
]

# Store level data
levels = [
    {"maze": maze_level_1, "start": (1, 1), "finish": (8, 9)},
    {"maze": maze_level_2, "start": (1, 1), "finish": (8, 9)}
]
current_level_index = 0

# Initialize scores for each level
scores = [[] for _ in levels]

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
            # Check if the coordinates are within maze bounds
            if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
                cell_type = maze[cell_y][cell_x]
                if cell_type == 0:
                    self.x = new_x
                    self.y = new_y
                elif cell_type == 3:
                    self.finish_level(new_x, new_y)
                elif cell_type == 9:
                    self.reset()  # Reset if moving into a hazardous area
            else:
                self.reset()  # Reset if moving outside the maze boundaries

    def finish_level(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        if not self.finished:
            elapsed_time = time.time() - self.start_time
            scores[current_level_index].append(elapsed_time)
            scores[current_level_index].sort()
            if len(scores[current_level_index]) > 3:
                scores[current_level_index].pop()
            self.finished = True
            print(f"Level {current_level_index + 1} completed in {elapsed_time:.2f} seconds")
            next_level()  # Call to change the level

    def reset(self):
        print("Blob has died! Resetting level...")
        self.load_level(current_level_index)



# Function to handle level switching and initialization
def next_level():
    global current_level_index, blob
    current_level_index = (current_level_index + 1) % len(levels)
    blob.reset()

# Function to draw controls and scores
def draw_text():
    screen.fill((0, 0, 0), (0, 0, 200, screen_height))  # Clear the sidebar area
    instructions = ["Controls:", "Shift + Arrow = Move", "R = Reset", "", "Top Times:"]
    y_offset = 20
    for text in instructions:
        instruction_text = font.render(text, True, (255, 255, 255))
        screen.blit(instruction_text, (30, y_offset))
        y_offset += 30
    
    # Display scores for the current level
    y_offset += 20  # Additional offset for scores section
    score_texts = ["Level 1:", "Level 2:"]
    for i, level_scores in enumerate(scores):
        level_text = font.render(score_texts[i], True, (255, 255, 255))
        screen.blit(level_text, (30, y_offset))
        y_offset += 30
        for score in level_scores[:3]:
            score_text = font.render(f"{score:.2f}s", True, (255, 255, 255))
            screen.blit(score_text, (50, y_offset))
            y_offset += 30

# Create the blob object for the initial level
blob = Blob(current_level_index)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:  # Reset the game when 'R' is pressed
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

    screen.fill((0, 0, 0))  # Clear the screen
    # Draw the current level's maze
    maze = levels[current_level_index]["maze"]
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, ((screen_width // 2 - len(maze[0]) * cell_size // 2) + x * cell_size, (screen_height // 2 - len(maze) * cell_size // 2) + y * cell_size, cell_size, cell_size))
    blob.draw()
    draw_text()
    pygame.display.update()
