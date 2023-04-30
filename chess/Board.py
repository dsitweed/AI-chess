from constants import *
from Square import Square
from Piece import *
from Move import Move
import copy


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        # Set row for pawn line and other chess pieces line
        # if White 1, 0 if black 6, 7  # Start 0 -> 7
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)


    def calc_moves(self, row, col, piece):
        """
        Calculate all the possible  (valid) moves of an specific piece on a specific position
        :param row: now row position
        :param col: now columns position
        :param piece: piece in chess board
        :return:
        """

        def pawn_moves():
            """
            complicated func. 3 step: use piece is instance of Pawn Class
            step 1: define step (1 or 2)
            step 2: vertical moves
            step 3: Diagonal moves
            :return:
            """
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves - Pawn has direction parameter
            start = row + piece.direction  # piece.direction = - 1 || 1
            end = row + piece.direction * (1 + steps)  # have end parameter for check if pawn moved to end of board
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create a new move
                        move = Move(initial, final)

                        # check potential
                        if True:
                            piece.add_move(move)
                    else:  # Not is empty = blocked
                        break
                else:  # Not in range
                    break


            # Diagonal moves


        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # Create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        # Create new move
                        move = Move(initial, final)
                        # Append a valid move
                        piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            pass

        elif isinstance(piece, Rook):
            pass

        elif isinstance(piece, Queen):
            pass

        elif isinstance(piece, King):
            pass


if __name__ == '__main__':
    board = Board()
    print(board.squares)
