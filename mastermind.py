import chess
import time
from eval_functions import *
from transposition import *

board = chess.Board()
time_limit = None
init_transposition_table()


def run_engine():
    reset_transposition_table()
    best_value = None
    best_move = None
    start_time = time.time()
    for depth in range(1, 7):
        engine = negamax(board, depth, -1000000, 1000000, False, start_time, time_limit)
        if engine:
            print(engine)
            (best_value, best_move) = engine
        else:
            return (best_value, best_move, depth - 1)


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
        moves = 0
        board.push_uci(command)
        if board.outcome():
            print(f"{board.outcome().termination.name}! {board.outcome().result()}")
            break
        if moves == 1:
            print("A")
        engine = run_engine()
        (engine_eval, engine_move, depth) = engine
        board.push(engine_move)
        print(f"({-engine_eval/100}) {engine_move}. Depth: {depth}")
        print(board)
        moves += 1
    except chess.IllegalMoveError:
        print("Illegal move")
    except chess.InvalidMoveError:
        print("Invalid UCI move")