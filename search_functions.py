import chess
import time
from eval_constants import *
from eval_functions import *
from order_functions import *
from transposition import *


def negamax(position: chess.Board, depth: int, alpha: int, beta: int, is_max_turn: bool, start_time: float|None, time_limit: int|None):
    if time_limit and start_time and time.time() - start_time >= time_limit:
        return None
    
    alpha_original = alpha
    
    tt_entry = search_transposition_table(position)
    if tt_entry and tt_entry["depth"] >= depth:
        # print("TT hit")
        if tt_entry["flag"] == "exact":
            return tt_entry["value"]
        elif tt_entry["flag"] == "lowerbound":
            alpha = max(alpha, tt_entry["value"])
        elif tt_entry["flag"] == "upperbound":
            beta = min(beta, tt_entry["value"])
        if alpha >= beta:
            return tt_entry["value"]

    if depth == 0:
        last_move = position.pop()
        if position.is_capture(last_move):
            position.push(last_move)
            return quiescence_search(position, alpha, beta, is_max_turn)
        else:
            position.push(last_move)
            return (evaluate_position(position, is_max_turn), None)

    legal_moves = order_moves(position)
    bestmove = None
    value = -1000000
    for node in legal_moves:
        if position.is_legal(node):
            position.push(node)
            evaluation = negamax(position, depth - 1, -beta, -alpha, not is_max_turn, start_time, time_limit)
            if evaluation is None:
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
                add_killer_move(node, position.ply())
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

def quiescence_search(position: chess.Board, alpha: int, beta: int, is_max_turn: bool):
    legal_moves = list(position.legal_moves)
    evaluation = evaluate_position(position, is_max_turn)
    if evaluation >= beta:
        return beta
    if alpha < evaluation:
        alpha = evaluation

    for legal_move in legal_moves:
        if board.is_capture(legal_move):
            position.push(legal_move)
            score = -quiescence_search(position, -beta, -alpha, not is_max_turn)
            position.pop()
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

    return alpha
