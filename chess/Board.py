from constants import *
from Square import Square
from Piece import *
from Move import Move
import copy


class Board:
    def __init__(self):
        """
        : last_move: save the nearest move
        """
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

    def check_promotion(self, piece, final):
        """
        If Pawn gone last row -> Can become other piece now just pawn -> Queen
        :param piece:
        :param final:
        :return: Pawn -> to Queen
        """
        if isinstance(piece, Pawn):
            row, col = final.row, final.col
            if row == 0 or row == 7:
                self.squares[row][col].piece = Queen(piece.color)

    def is_castling(self, initial, final):
        """
        Check move for castling is a valid move ?
        :param initial: initial move
        :param final: final move
        :return:
        """
        # Check Rule: King can not move onto checking square
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        """
        Set all Pawn pieces -> False just selected piece have en_passant = True
        :param piece:
        :return: 1 Pawn have 1 chance en_passant = True when move in fist time
        """
        if not isinstance(piece, Pawn):
            return

        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True

    def in_check(self, piece, move):
        """
        Check in chess - not a normal check
        :parameter piece: is selecting piece
        :parameter move: will select move
        :return: Boolean
        """
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    piece_ = temp_board.squares[row][col].piece
                    temp_board.calc_moves(row, col, piece_, check=False)

                    for m in piece_.moves:
                        if isinstance(m.final.piece, King):
                            return True  # King is checking by enemy piece

        return False

    def calc_moves(self, row, col, piece, check=True):
        """
        Calculate all the possible  (valid) moves of an specific piece on a specific position
        and add all possible moves -> piece.moves
        :param row: now row position
        :param col: now columns position
        :param piece: piece in chess board
        :param check: Check now king is being check # Kiểm tra xem hiện tại (vua) có đang bị chiếu không
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

                        # check potential checks
                        # Kiểm tra xem có đang bị chiếu không
                        if check:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            # Append new move
                            piece.add_move(move)
                    else:  # Not is empty = blocked
                        break
                else:  # Not in range
                    break

            # Diagonal moves
            possible_move_row = row + piece.direction
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_col, possible_move_row):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if check:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                        else:
                            # Append new move
                            piece.add_move(move)

                # En passant moves


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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create new move
                        move = Move(initial, final)

                        # check potencial checks
                        if check:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                        else:
                            # Append new move
                            piece.add_move(move)

        def straight_line_moves(increments):
            """
            Killed three bird in one shot - For Bishop, Rook and Queen
            :param increments: List of base move
            :return: No - available add move to piece
            """
            for increment in increments:
                row_incr, col_incr = increment
                possible_row = row + row_incr
                possible_col = col + col_incr

                """
                Why here we use while True. Because increments parameter just list of base move (move 1 step)
                So we want to check all of available move multiple step
                """
                while True:
                    if Square.in_range(possible_row, possible_col):
                        # Create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col, final_piece)
                        # Create new possible new move
                        move = Move(initial, final)

                        # Empty = continue looping
                        if self.squares[possible_row][possible_col].is_empty():
                            # print(f"{possible_col} - {possible_row}")
                            # check potencial checks
                            if check:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # Has enemy piece = add move + break
                        elif self.squares[possible_row][possible_col].has_enemy_piece(piece.color):
                            # check potencial checks
                            if check:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            # Have enemy piece -> add move + break
                            break

                        # Has team piece = break
                        elif self.squares[possible_row][possible_col].has_team_piece(piece.color):
                            break
                    else:  # not in range
                        break

                    # Incrementing from base move
                    possible_row = possible_row + row_incr
                    possible_col = possible_col + col_incr

        def king_moves():
            adjacent = [
                (row - 1, col + 0),  # Up
                (row - 1, col + 1),  # up-right
                (row + 1, col + 0),  # down
                (row + 1, col + 1),  # down-right
                (row + 0, col + 1),  # right
                (row + 0, col - 1),  # left
                (row - 1, col - 1),  # up-left
                (row + 1, col - 1),  # down-left
            ]

            # Normal moves
            for possible_move in adjacent:
                possible_row, possible_col = possible_move

                if Square.in_range(possible_row, possible_col):
                    if self.squares[possible_row][possible_col].is_empty_or_enemy(piece.color):
                        # Create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col)  # piece = piece
                        # create new move
                        move = Move(initial, final)

                        # check potential checks
                        if check:
                            if not self.in_check(piece, move):
                                # append new valid move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

                    else:  # have team piece = continue
                        continue
                else:  # not in range
                    continue

            # Castling moves
            """
            If king not moved -> king can castle
            -> Add more valid move for king piece and rook move
            4 rule: 
                1. Your king and rook can not have moved
                2. Your king can NOT be in check
                3. Your king can not pass through check, King can not move onto checking square
                4. No pieces can be between the king and rook
            """
            if not piece.moved:  # piece is instance of King class
                # King is in check ?
                initial = Square(row, col)
                final = Square(row, col)
                move = Move(initial, final)
                if self.in_check(piece, move):  # If in checking can't castle
                    return

                # Queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            # Check rule 3
                            if c != 1:
                                initial_ = Square(row, col)
                                final_ = Square(row, c)
                                move_ = Move(initial_, final_)
                                if self.in_check(piece, move_):
                                    break

                            if c == 3:
                                # King move
                                piece.can_castle = True  # False as default of King Piece
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # Adds left rook to king
                                piece.left_rook = left_rook

                                # Rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # Add moves
                                left_rook.add_move(moveR)
                                piece.add_move(moveK)

                # King castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            # castling is not possible because there are pieces in between
                            if self.squares[row][c].has_piece():
                                break

                            # Check Rule 3
                            initial_ = Square(row, col)
                            final_ = Square(row, c)
                            move_ = Move(initial_, final_)
                            if self.in_check(piece, move_):
                                break

                            if c == 6:
                                # King move
                                piece.can_castle = True  # False as default of King Piece
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # Adds right rook to king
                                piece.right_rook = right_rook

                                # Rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)



                                # Adds moves
                                # Append new move to King
                                piece.add_move(moveK)
                                # Append new move to Rook
                                right_rook.add_move(moveR)

        # Switch each type of piece (type Class) for each type of moves
        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straight_line_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
            ])

        elif isinstance(piece, Rook):
            straight_line_moves([
                (0, 1),  # go right
                (0, -1),  # go left
                (1, 0),  # go down
                (-1, 0),  # go up
            ])

        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1, 1),  # up-right
                (-1, -1),  # up-left
                (1, 1),  # down-right
                (1, -1),  # down-left
                (0, 1),  # go right
                (0, -1),  # go left
                (1, 0),  # go down
                (-1, 0),  # go up
            ])

        elif isinstance(piece, King):
            king_moves()

    def valid_move(self, piece, move):
        return move in piece.moves

    def move(self, piece, move):
        initial, final = move.initial, move.final

        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Pawn special moves
        if isinstance(piece, Pawn):
            # en passant capture

            # pawn promotion
            self.check_promotion(piece, final)

        # King castling
        if isinstance(piece, King):
            if piece.can_castle and self.is_castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if diff < 0 else piece.right_rook
                # Move for rook
                self.move(rook, rook.moves[0])

        # Piece moved
        piece.moved = True

        # Clear valid moves
        piece.clear_moves()

        # Save last move
        self.last_move = move


if __name__ == '__main__':
    board = Board()
    print(board.squares)
