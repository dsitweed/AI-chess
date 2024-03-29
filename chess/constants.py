import os.path
import pygame


SEARCHING = "searching"
NODE_STATE = ["source", "goal"]
NODE_EMPTY = "empty"

GOAL = "goal"
SOURCE = "source"
SUCCESS = "success"
FAILED = "failed"

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // ROWS  # cell size
FPS = 60

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

LIGHT_GREEN = (234, 235, 200)
DARK_GREEN = (119, 154, 88)

