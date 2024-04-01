import chess
import time
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

    
def negamax(position: chess.Board, depth: int, alpha: int, beta: int, is_max_turn: bool, start_time: time.time, time_limit: int):
    if time.time() - start_time >= time_limit:
        return None
    
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
        evaluation = negamax(position, depth - 1, -beta, -alpha, not is_max_turn, start_time, time_limit)
        if not evaluation:
            position.pop()
            return None
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