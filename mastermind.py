import chess
import time
from search_functions import *
from transposition import *

board = chess.Board()
time_limit = None
init_transposition_table()


def run_engine():
    reset_transposition_table()
    best_value = None
    best_move = None
    start_time = time.time()
    for depth in range(1, 4):
        engine = negamax(board, depth, -1000000, 1000000, False, start_time, time_limit)
        if engine:
            print(engine)
            (best_value, best_move) = engine
        else:
            return (best_value, best_move, depth - 1)
    return (best_value, best_move, depth)


while True:
    command = input().strip()
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