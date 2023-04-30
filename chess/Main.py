import pygame
import sys
from constants import *
from Game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('AI Chess')
        self.game = Game()

    def main_loop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger



        while True:
            # Show a game screen
            game.show_board(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():

                # Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouse_y // SQUARE_SIZE
                    clicked_col = dragger.mouse_x // SQUARE_SIZE

                    # If clicked square has a piece ?
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # Calculate valid move
                        board.calc_moves(clicked_row, clicked_col, piece)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)
                        # Show method
                        game.show_board(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        print(f"{board.squares[clicked_row][clicked_col].col} - {board.squares[clicked_row][clicked_col].row} - {dragger.dragging}")
                        # Valid piece (color) ?



                # Mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_col = event.pos[0] // SQUARE_SIZE
                    motion_row = event.pos[1] // SQUARE_SIZE

                    # game.set_hover(motion_row, motion_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_board(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                # Mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update all changes to the pygame.surface
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.main_loop()
