import chess
from eval_constants import *
from transposition import *

game_phase = "mg"


def evaluate_position(position: chess.Board, is_max_turn: bool):
    if position.is_checkmate():
            return 20000
    else:
        evaluation = 0
        base_board = chess.BaseBoard(position.board_fen())
        piece_map = base_board.piece_map()
        for piece_index in piece_map:
            piece = piece_map[piece_index]
            if is_max_turn:
                if piece.color == chess.WHITE:
                    evaluation += PIECE_VALUES[game_phase][piece.symbol()]
                    evaluation += WHITE_SQUARE_TABLES[piece.symbol()][game_phase][8 - piece_index >> 3][8 - piece_index & 7]
                else:
                    evaluation -= PIECE_VALUES[game_phase][piece.symbol().upper()]
                    evaluation -= BLACK_SQUARE_TABLES[piece.symbol().upper()][game_phase][piece_index >> 3][piece_index & 7]
            else:
                if piece.color == chess.WHITE:
                    evaluation -= PIECE_VALUES[game_phase][piece.symbol()]
                    evaluation -= WHITE_SQUARE_TABLES[piece.symbol()][game_phase][8 - piece_index >> 3][8 - piece_index & 7]
                else:
                    evaluation += PIECE_VALUES[game_phase][piece.symbol().upper()]
                    evaluation += BLACK_SQUARE_TABLES[piece.symbol().upper()][game_phase][piece_index >> 3][piece_index & 7]
        return evaluation


# def alphabeta(position: chess.Board, last_move_was_capture: bool, depth: int, alpha: int, beta: int, is_max_turn: bool):
#     if depth == 0:
#         return (evaluate_position(position, is_max_turn), None)

#     legal_moves = list(position.legal_moves)
#     bestmove = None
#     if last_move_was_capture:
#         capture_square = position.peek().to_square
#         for square in position.attackers(position.turn, capture_square):
#             if position.piece_at(square).symbol().upper() == "K":
#                 try:
#                     position.find_move(square, capture_square)
#                 except chess.IllegalMoveError:
#                     continue
#             move = chess.Move(square, capture_square)
#             legal_moves.pop(legal_moves.index(move))
#             legal_moves.insert(0, move)
            
#     if is_max_turn:
#         value = -1000000
#         for node in legal_moves:
#             is_capture = position.is_capture(node)
#             position.push(node)
#             eval = alphabeta(position, is_capture, depth - 1, -1000000, 1000000, False)
#             value = max(value, eval[0])
#             position.pop()
#             if value > alpha:
#                 bestmove = node
#                 alpha = value
#                 if alpha >= beta:
#                     break
                
#     else:
#         value = 1000000
#         for node in legal_moves:
#             is_capture = position.is_capture(node)
#             position.push(node)
#             eval = alphabeta(position, is_capture, depth - 1, -1000000, 1000000, True)
#             value = min(value, eval[0])
#             position.pop()
#             if value < beta:
#                 bestmove = node
#                 beta = value
#                 if alpha >= beta:
#                     break
#     return (value, bestmove)
    
def negamax(position: chess.Board, depth: int, alpha: int, beta: int, is_max_turn: bool):
    alpha_original = alpha
    
    tt_entry = search_transposition_table(position)
    if tt_entry and tt_entry["depth"] >= depth:
        print("TT hit")
        if tt_entry["flag"] == "exact":
            return tt_entry["value"]
        elif tt_entry["flag"] == "lowerbound":
            alpha = max(alpha, tt_entry["value"])
        elif tt_entry["flag"] == "upperbound":
            beta = min(beta, tt_entry["value"])
        if alpha >= beta:
            return tt_entry["value"]

    if depth == 0:
        return (evaluate_position(position, is_max_turn), None)

    legal_moves = list(position.legal_moves)
    bestmove = None
    value = -1000000
    for node in legal_moves:
        position.push(node)
        evaluation = negamax(position, depth - 1, -beta, -alpha, not is_max_turn)
        if type(evaluation) == tuple:
            evaluation = -evaluation[0]
        else:
            evaluation = -evaluation
        if evaluation > value:
            value = evaluation
            bestmove = node
        alpha = max(alpha, value)
        position.pop()
        if alpha >= beta:
            break
    
    tt_entry = {}
    tt_entry["value"] = value
    if value <= alpha_original:
        tt_entry["flag"] = "upperbound"
    elif value >= beta:
        tt_entry["flag"] = "lowerbound"
    else:
        tt_entry["flag"] = "exact"
    tt_entry["depth"] = depth
    store_transposition_table(position, tt_entry)

    return (value, bestmove)
