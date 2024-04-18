import pygame
import time

pygame.init()

# Set up the screen
screen_width = 1000  # Increased width to accommodate score table
screen_height = 600
cell_size = 40  # Size of each cell in the maze

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game with Scores")

# Define the maze layout
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 1, 1, 0, 0, 0, 0, 1],  # Start point
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 1, 1, 3, 1],  # Finish point
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Score tracking
scores = []

# Font for text rendering
font = pygame.font.Font(None, 36)

# Calculate offsets to center the maze
maze_offset_x = (screen_width - len(maze[0]) * cell_size) // 2 + 200  # Adjust to fit score table
maze_offset_y = (screen_height - len(maze) * cell_size) // 2

class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = cell_size
        self.color = (0, 255, 0)  # Green
        self.start_time = None
        self.finished = False

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move(self, dx, dy):
        if not self.finished:
            new_x = self.x + dx
            new_y = self.y + dy
            # Check if the new position is within a walkable cell
            cell_x = (new_x - maze_offset_x) // cell_size
            cell_y = (new_y - maze_offset_y) // cell_size
            if 0 <= cell_x < len(maze[0]) and 0 <= cell_y < len(maze):
                if maze[cell_y][cell_x] == 0:
                    self.x = new_x
                    self.y = new_y
                elif maze[cell_y][cell_x] == 3:
                    self.x = new_x
                    self.y = new_y
                    if self.start_time and not self.finished:
                        elapsed_time = time.time() - self.start_time
                        scores.append(elapsed_time)
                        scores.sort()
                        if len(scores) > 3:
                            scores.pop(-1)
                        self.finished = True

    def reset(self):
        # Reset the blob to the starting position and restart the timer
        start_x, start_y = next((x * cell_size, y * cell_size) for y, row in enumerate(maze) for x, val in enumerate(row) if val == 2)
        self.x = maze_offset_x + start_x
        self.y = maze_offset_y + start_y
        self.start_time = None
        self.finished = False

# Initialize the blob at the start point
start_x, start_y = next((x * cell_size, y * cell_size) for y, row in enumerate(maze) for x, val in enumerate(row) if val == 2)
blob = Blob(maze_offset_x + start_x, maze_offset_y + start_y)

def draw_text():
    screen.fill((0, 0, 0), (0, 0, 200, screen_height))  # Clear the left side area
    # Instructions for playing
    instructions = [
        "Controls:",
        "Shift + Arrow = Move",
        "R = Reset",
        "",
        "Top Times:"
    ]

    # Draw instructions and controls
    for i, text in enumerate(instructions):
        instruction_text = font.render(text, True, (255, 255, 255))
        screen.blit(instruction_text, (30, 120 + 30 * i))

    # Draw top scores
    for j, score in enumerate(scores):
        score_text = font.render(f"{j + 1}. {score:.2f}s", True, (255, 255, 255))
        screen.blit(score_text, (30, 280 + 40 * j))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:  # Reset the game when 'R' is pressed
        blob.reset()

    if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and not blob.start_time and not blob.finished:
        blob.start_time = time.time()  # Start the timer on first valid move with Shift
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
        if keys[pygame.K_LEFT]:
            blob.move(-cell_size, 0)
        if keys[pygame.K_RIGHT]:
            blob.move(cell_size, 0)
        if keys[pygame.K_UP]:
            blob.move(0, -cell_size)
        if keys[pygame.K_DOWN]:
            blob.move(0, cell_size)

    # Clear the entire screen and redraw elements
    screen.fill((0, 0, 0))
    
    # Draw the maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            pygame.draw.rect(screen, color, (maze_offset_x + x * cell_size, maze_offset_y + y * cell_size, cell_size, cell_size))
    
    # Draw the blob
    blob.draw()

    # Draw the scores
    draw_text()
    
    # Update the display
    pygame.display.update()

pygame.quit()

