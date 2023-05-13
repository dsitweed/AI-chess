import chess
import chess.polyglot  # for read moves from books
import chess.engine

# Bảng chấm điểm theo vị trí từng quân cờ nhìn từ góc độ của quân TRẮNG
# Vị trí cột tương ứng với vị trí của cột trong bàn cở
pawns_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knights_table = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bishops_table = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rooks_table = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

queens_table = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

kings_table = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


def check_game(board: chess.Board):
    turn = 'white'
    if board.is_check():
        if board.turn:
            return -9999
        else:
            return 9999  # White win

    if board.is_stalemate():
        return 0

    if board.is_insufficient_material():
        return 0


# TÍnh toán các tri thức bổ sung hỗ trợ việc đưa ra quyết định
def evaluation(board: chess.Board):
    """
    Calculate heuristic for the game
    :param board:
    :return:
    """
    white_pawn = len(board.pieces(chess.PAWN, chess.WHITE))
    black_pawn = len(board.pieces(chess.PAWN, chess.BLACK))
    white_knight = len(board.pieces(chess.KNIGHT, chess.WHITE))
    black_knight = len(board.pieces(chess.KNIGHT, chess.BLACK))
    white_bishop = len(board.pieces(chess.BISHOP, chess.WHITE))
    black_bishop = len(board.pieces(chess.BISHOP, chess.BLACK))
    white_rook = len(board.pieces(chess.ROOK, chess.WHITE))
    black_rook = len(board.pieces(chess.ROOK, chess.BLACK))
    white_queen = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queen = len(board.pieces(chess.QUEEN, chess.BLACK))

    material_score = 100 * (white_pawn - black_pawn) + 320 * (white_knight - black_knight) \
            + 330 * (white_bishop - black_bishop) + 500 * (white_rook - black_rook) + 900 * (white_queen - black_queen)

    # Individual pieces score
    pawn_sq = sum([pawns_table[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawn_sq = pawn_sq + sum([-pawns_table[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])

    knight_sq = sum([knights_table[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knight_sq = knight_sq + sum([-knights_table[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])

    bishop_sq = sum([bishops_table[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishop_sq = bishop_sq + sum([-bishops_table[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])

    rook_sq = sum([rooks_table[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rook_sq = rook_sq + sum([-rooks_table[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])

    queen_sq = sum([queens_table[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queen_sq = queen_sq + sum([-queens_table[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])

    king_sq = sum([kings_table[i] for i in board.pieces(chess.KING, chess.WHITE)])
    king_sq = king_sq + sum([-kings_table[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])

    evaluation_score = material_score + pawn_sq + knight_sq + bishop_sq + rook_sq + queen_sq + king_sq

    if board.turn:  # WHITE turn
        return evaluation_score
    else:
        return -evaluation_score


def get_moves_in_book(board: chess.Board, path='../assets/books/human.bin'):
    list_path = [
        '../assets/books/human.bin',
        '../assets/books/computer.bin',
        '../assets/books/pecg_book.bin'
    ]
    try:
        move_from_book = chess.polyglot.MemoryMappedReader(path).weighted_choice(board=board).move
        return move_from_book
    except FileNotFoundError:
        print("HAVE ERROR WHEN READ BOOK")

def select_move(board: chess.Board, depth):
    try:
        best_move = chess.Move.null()
        best_value = -99999
        alpha = -99999
        beta = 99999
        for move in board.legal_moves:
            board.push(move)
            board_value = - alpha_beta(board, -beta, -alpha, depth - 1)
            if board_value > best_value:
                best_value = board_value
                best_move = move
            if board_value > alpha:
                alpha = board_value

            board.pop()
            return best_move
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def alpha_beta(board : chess.Board, alpha, beta, depth_left):
    best_score = -9999
    if depth_left == 0:
        return quiesce(board, alpha, beta)

    for move in board.legal_moves:
        board.push(move)
        score = - alpha_beta(board, -beta, -alpha, depth_left -1)
        board.pop()

        if score >= beta:
            return score
        if score > best_score:
            best_score = score
        if score > alpha:
            alpha = score

    return best_score


def quiesce(board, alpha, beta):
    stand_pat = evaluation(board)
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat

    for move in board.legal_moves:
        if board.is_capture(move):
            board.push(move)
            score = - quiesce(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha


# Speak Function for the Assistant to speak
def speak(text):
    pass


def test_AI_human():
    board = chess.Board()
    move = select_move(3)
    board.push(move)

    board.push_san('e5')
        



if __name__ == '__main__':
    speak()

