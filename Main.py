import pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
cell_size = 40  # Size of each cell in the maze
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Blob:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = (0, 255, 0)  # Green

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
        return True

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Green Blob Maze Game")
running = True

# Find an empty cell for the starting position of the blob
blob_start_x, blob_start_y = 0, 0
while maze[blob_start_y][blob_start_x] != 0:
    blob_start_x += 1
    if blob_start_x >= len(maze[0]):
        blob_start_x = 0
        blob_start_y += 1
    if blob_start_y >= len(maze):
        raise ValueError("No empty cell found for blob's starting position.")

# Create the blob
blob = Blob(blob_start_x * cell_size, blob_start_y * cell_size)

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
