

class Square:
    ALPHA_COLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alpha_col = self.ALPHA_COLS[col]

    def has_piece(self):
        return self.piece is not None

    def __eq__(self, other):
        """
        When use == allows to compare two objects of that class for equality.
        :param other: other object
        :return: Boolean
        """
        return self.row == other.row and self.col == other.col

    def is_empty(self):
        return not self.has_piece()

    def is_empty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy_piece(color)

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color

    @staticmethod
    def in_range(*args):
        """
        check position is in board range ?
        :param args: a list position
        :return: Boolean
        """
        for arg in args:
            if arg < 0 or arg > 7:
                return False

        return True

    @staticmethod
    def get_alpha_col(col):
        ALPHA_COLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        return ALPHA_COLS[col]
