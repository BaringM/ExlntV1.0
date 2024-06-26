# Levels.py

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

maze_level_2 = [
    [1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 9, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
]

maze_level_3 = [
    [1, 9, 9, 9, 9, 9, 1, 9, 9, 9, 1],
    [1, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 9, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 9, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1]
]

levels = [
    {"maze": maze_level_1, "start": (1, 1), "finish": (8, 9)},
    {"maze": maze_level_2, "start": (1, 1), "finish": (8, 9)}
]

def get_levels():
    return levels
