import pygame
import time

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
cell_size = 40  # Size of each cell in the maze
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

class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = (0, 255, 0)  # Green
        self.start_time = None

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def can_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Calculate the corners of the new position
        top_left = (new_x, new_y)
        top_right = (new_x + self.size - 1, new_y)
        bottom_left = (new_x, new_y + self.size - 1)
        bottom_right = (new_x + self.size - 1, new_y + self.size - 1)
        
        # Calculate the cell indices of the corners
        corners = [top_left, top_right, bottom_left, bottom_right]
        for corner in corners:
            cell_x = corner[0] // cell_size
            cell_y = corner[1] // cell_size
            if maze[cell_y][cell_x] == 1:
                return False
            elif maze[cell_y][cell_x] == 3:
                self.stop_timer()  # Stop timer when reaching the finish
        return True
    
    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            print("Congratulations! You completed the maze in {:.2f} seconds.".format(elapsed_time))
            self.start_time = None

# Find the starting position marked as '2' in the maze
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 2:
            blob_start_x = x * cell_size
            blob_start_y = y * cell_size
            break
    else:
        continue
    break

# Create the blob at the starting position
blob = Blob(blob_start_x, blob_start_y)

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Green Blob Maze Game")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Check if Shift key is held down
        if keys[pygame.K_LEFT]:
            if blob.can_move(-5, 0):
                blob.x -= 5
        if keys[pygame.K_RIGHT]:
            if blob.can_move(5, 0):
                blob.x += 5
        if keys[pygame.K_UP]:
            if blob.can_move(0, -5):
                blob.y -= 5
        if keys[pygame.K_DOWN]:
            if blob.can_move(0, 5):
                blob.y += 5

    # Start timer when moving from the start point
    if maze[blob.y // cell_size][blob.x // cell_size] == 2 and blob.start_time is None:
        blob.start_timer()

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw the maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255), (x * cell_size, y * cell_size, cell_size, cell_size))

    # Draw the blob
    blob.draw(screen)

    # Update the display
    pygame.display.update()

pygame.quit()
