import pygame
from constants import *


class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0

    # Blit method - draw one image onto another
    def update_blit(self, surface):
        if self.piece is not None:
            self.piece.set_texture(size=128)
            # Texture
            texture = self.piece.texture
            # Image
            img = pygame.image.load(texture)
            # Rect
            img_center = (self.mouse_x, self.mouse_y)
            self.piece.texture_rect = img.get_rect(center=img_center)
            # Blit
            surface.blit(img, self.piece.texture_rect)

    def update_mouse(self, position):
        self.mouse_x, self.mouse_y = position  # (xcor, ycor)

    def save_initial(self, position):
        self.initial_col = position[0] // SQUARE_SIZE
        self.initial_row = position[1] // SQUARE_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False
