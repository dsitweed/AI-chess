import pygame
import os.path
from Dragger import Dragger
from constants import *
from Board import Board
from Config import Config
from Square import Square


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # Show board
    def show_board(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = theme.background.light  # Light color
                else:
                    color = theme.background.dark  # Dark color

                # x axios, y axios, width, height
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.background.dark if (row + col) % 2 == 0 else theme.background.light
                    # label -> can be seen that the index of the chessboard is opposite to the index of row
                    label = self.config.font.render(str(ROWS - row), 1, color)
                    label_position = (5, 5 + row * SQUARE_SIZE)
                    # blit
                    surface.blit(label, label_position)

                # Col coordinates
                if row == 7:
                    # color
                    color = theme.background.dark if (row + col) % 2 == 0 else theme.background.light
                    # label
                    label = self.config.font.render(Square.get_alpha_col(col), 1, color)
                    label_position = (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20)
                    # blit
                    surface.blit(label, label_position)

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
        Show all valid moves of dragging piece
        :param surface: surface for render - is a instance of Board class
        :return:
        """
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece

            # Loop all valid moves
            for move in piece.moves:
                row, col = move.final.row, move.final.col
                # 3 step: define color -> rect -> blit. Like show_board
                color = theme.moves.light if ((row + col) % 2 == 0) else theme.moves.dark  # Light color or Dark color
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # Color
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark # Light color or Dark color
                # Rect
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                # blit
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = "#C86464"
            rect = (self.hovered_sqr.col * SQUARE_SIZE, self.hovered_sqr.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            # Blit
            pygame.draw.rect(surface, color, rect, width=3)

    # Other method - Not render method
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:  # Play move sound
            self.config.move_sound.play()

    def reset(self):
        self.__init__()
