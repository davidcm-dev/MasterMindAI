import chess

board = chess.Board(fen="k1q3r1/ppp5/1n6/5N2/8/8/5PPP/5RQK w - - 0 1")


def engine_move():
    print(alphabeta(board, 3, -1000000, 1000000, False))


def evaluate_position(position: chess.Board):
    evaluation = 0
    piece_values = {
        "P": 100,
        "N": 300,
        "B": 300,
        "R": 500,
        "Q": 900,
        "K": 20000,
        "p": -100,
        "n": -300,
        "b": -300,
        "r": -500,
        "q": -900,
        "k": -20000,
    }
    base_board = chess.BaseBoard(position.board_fen())
    for piece in list(base_board.piece_map().values()):
        evaluation += piece_values[piece.symbol()]
    return evaluation


def alphabeta(position: chess.Board, depth:int, alpha:int, beta:int, is_max_turn:bool):
    legal_moves = list(position.legal_moves)
    if depth == 0:
        return (evaluate_position(position), None)
    
    bestmove = None
    if is_max_turn:
        value = -1000000
        for node in legal_moves:
            board = position.copy()
            board.push(node)
            eval = alphabeta(board, depth - 1, -1000000, 1000000, False)
            value = max(value, eval[0])
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
        engine_move()
    except chess.IllegalMoveError:
        print("Illegal move")
    except chess.InvalidMoveError:
        print("Invalid UCI move")
