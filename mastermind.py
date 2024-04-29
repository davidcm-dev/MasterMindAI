import chess
import time
from search_functions import *
from transposition import *

board = chess.Board()
init_transposition_table()


def calc_time_limit(go_command: str):
    if "wtime" in go_command:
        cmd = go_command[go_command.find("wtime"):].strip().split(" ") # ["wtime", int, "btime", int, "winc", int, "binc", int]
        if board.turn == chess.WHITE:
            return int(cmd[1])/1000/(50-board.fullmove_number)
        else:
            return int(cmd[3])/1000/(50-board.fullmove_number)
    else:
        return 5


def run_engine(time_limit: int):
    reset_transposition_table()
    best_value = None
    best_move = None
    start_time = time.time()
    for depth in range(1, 100):
        engine = negamax(board, depth, -1000000, 1000000, board.turn, start_time, time_limit)
        if engine:
            (best_value, best_move) = engine
        else:
            return (best_value, best_move, depth - 1)
    return (best_value, best_move, depth)


while True:
    command = input().strip()
    if command == "uci":
        print("id name MasterMind AI")
        print("id author davidcm-dev")
        print("uciok")

    if command == "isready":
        print("readyok")

    if command == "ucinewgame":
        board.reset()

    if "position" in command:
        if "startpos" in command:
            board.reset()
        else:
            fen = command[command.find("fen") + 10:command.find("moves")].strip()
            board.set_fen(fen)
        try:
            moves = command[command.index("moves") + 6:]
            for move in moves.split(" "):
                board.push_uci(move.strip())
        except ValueError:
            pass

    if "go" in command:
        engine = run_engine(calc_time_limit(command))
        (engine_eval, engine_move, depth) = engine
        board.push(engine_move)
        print("bestmove " + engine_move.uci()) 

    if command == "quit":
        break
