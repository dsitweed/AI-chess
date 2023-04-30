import pygame
import os.path
from Dragger import Dragger
from constants import *
from Board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()

    # Show board
    def show_board(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = LIGHT_GREEN
                else:
                    color = DARK_GREEN

                # x axios, y axios, width, height
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # Piece?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    # All pieces except dragger piece
                    if piece is not self.dragger.piece:
                        # Set size of pieces 80 by default - When dragging is a litter bigger
                        piece.set_texture(80)

                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        # print(f"Rect: {piece.texture_rect}")
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        """
        Show all valid moves
        :param surface: surface for render - is a instance of Board class
        :return:
        """
        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop all valid moves
            for move in piece.moves:
                row, col = move.final.row, move.final.col
                # 3 step: define color -> rect -> blit. Like show_board
                color = "#C86464" if ((row + col) % 2 == 0) else "#C84646"
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)
