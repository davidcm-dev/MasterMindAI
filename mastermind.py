import chess
from eval_functions import *
from transposition import *

board = chess.Board()
init_transposition_table()

def engine_move():  
    reset_transposition_table() 
    return negamax(board, 4, -1000000, 1000000, False)


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
        engine_response = engine_move()[1]
        board.push(engine_response)
        print(engine_response)
        print(board)
    except chess.IllegalMoveError:
        print("Illegal move")
    except chess.InvalidMoveError:
        print("Invalid UCI move")
