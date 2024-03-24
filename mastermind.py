import chess
from eval_constants import *

board = chess.Board()

game_phase = "mg"


def engine_move():
    return alphabeta(board, 3, -1000000, 1000000, False)


def evaluate_position(position: chess.Board, is_max_turn: bool):
    if position.is_checkmate():
        if is_max_turn:
            return -20000
        else:
            return 20000
    else:
        evaluation = 0
        base_board = chess.BaseBoard(position.board_fen())
        piece_map = base_board.piece_map()
        for piece_index in piece_map:
            piece = piece_map[piece_index]
            if piece.color == chess.WHITE:
                evaluation += PIECE_VALUES[game_phase][piece.symbol()]
                evaluation += WHITE_SQUARE_TABLES[piece.symbol()][game_phase][8 - piece_index >> 3][8 - piece_index & 7]
            else:
                evaluation -= PIECE_VALUES[game_phase][piece.symbol().upper()]
                evaluation -= BLACK_SQUARE_TABLES[piece.symbol().upper()][game_phase][8 - piece_index >> 3][8 - piece_index & 7]
        return evaluation


def alphabeta(position: chess.Board, depth: int, alpha: int, beta: int, is_max_turn: bool):
    legal_moves = list(position.legal_moves)
    if depth == 0:
        return (evaluate_position(position, is_max_turn), None)

    bestmove = None
    if is_max_turn:
        value = -1000000
        for node in legal_moves:
            position.push(node)
            eval = alphabeta(position, depth - 1, -1000000, 1000000, False)
            value = max(value, eval[0])
            position.pop()
            if value > alpha:
                bestmove = node
                alpha = value
                if alpha >= beta:
                    break
    else:
        value = 1000000
        for node in legal_moves:
            board = position.copy()
            board.push(node)
            eval = alphabeta(board, depth - 1, -1000000, 1000000, True)
            value = min(value, eval[0])
            if value < beta:
                bestmove = node
                beta = value
                if alpha >= beta:
                    break
    return (value, bestmove)


while True:
    command = input().strip()
    # if command == "uci":
    #     print("id name MasterMind\n")
    #     print("id author davidcm-dev\n")
    #     print("uciok\n")
    # if command == "isready":
    #     print("readyok\n")
    # if command == "ucinewgame":
    #     board.reset()
    # if "position" in command:
    #     moves = command[command.find("moves") + 6:].split()
    #     if "startpos" in command:
    #         for move in moves:
    #             board.push_uci(move)
    #         print(board)
    #     else:
    #         fen = command[13:command.find("moves") - 1]
    #         board.set_fen(fen)
    #         for move in moves:
    #             board.push_uci(move)
    #         print(board)
    # if "go" in command:
    #     legal_moves = [move.uci() for move in list(board.legal_moves)]
    #     print(random.choice(legal_moves))
    try:
        board.push_uci(command)
        if board.outcome():
            print(f"{board.outcome().termination.name}! {board.outcome().result()}")
            break
        move = engine_move()[1]
        board.push(move)
        print(move)
        print(board)
    except chess.IllegalMoveError:
        print("Illegal move")
    except chess.InvalidMoveError:
        print("Invalid UCI move")
