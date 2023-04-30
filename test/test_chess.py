import chess
import chess.svg

if __name__ == "__main__":
    board = chess.Board()
    svg_board = chess.svg.board(board=board)
    with open("./test/board.svg", "w") as f:
        f.write(svg_board)