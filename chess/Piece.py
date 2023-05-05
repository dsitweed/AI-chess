import os.path


class Piece:  # Abstract class
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        """
        :param name: Name
        :param color: color white or black
        :param value: each piece has difference value to AI process
        :param texture: Link to find actual image store place
        :param texture_rect: Rect(left, top, width, height) store position and size of piece
        """
        self.name = name
        self.color = color
        # If White -> positive
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.texture = texture
        self.texture_rect = texture_rect

        self.moves = []  # List valid moves
        self.moved = False
        self.set_texture()

    def set_texture(self, size=80):
        self.texture = os.path.join(f'../assets/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []


class Pawn(Piece):
    def __init__(self, color):
        super().__init__('pawn', color, 1.0)
        # Direction for Pawn if White -> down
        self.direction = -1 if color == 'white' else 1
        # pawn reaches end
        self.en_passant = False


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)


class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 10000.0)
        self.left_rook = None
        self.right_rook = None
        self.can_castle = False
