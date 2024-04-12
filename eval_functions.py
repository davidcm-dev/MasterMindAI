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


def order_moves(position: chess.Board):
    def calc_move_value(move: chess.Move):
        ## Victim, attacker ##
        mvv_lva_table = {
            chess.QUEEN: {
                chess.KING: 50, 
                chess.QUEEN: 51, 
                chess.ROOK: 52, 
                chess.BISHOP: 53, 
                chess.KNIGHT: 54, 
                chess.PAWN: 55
            },
            chess.ROOK: {
                chess.KING: 40, 
                chess.QUEEN: 41, 
                chess.ROOK: 42, 
                chess.BISHOP: 43, 
                chess.KNIGHT: 44, 
                chess.PAWN: 45
            },
            chess.BISHOP: {
                chess.KING: 30, 
                chess.QUEEN: 31, 
                chess.ROOK: 32, 
                chess.BISHOP: 33, 
                chess.KNIGHT: 34, 
                chess.PAWN: 35
            },
            chess.KNIGHT: {
                chess.KING: 20, 
                chess.QUEEN: 21, 
                chess.ROOK: 22, 
                chess.BISHOP: 23, 
                chess.KNIGHT: 24, 
                chess.PAWN: 25
            },
            chess.PAWN: {
                chess.KING: 10, 
                chess.QUEEN: 11, 
                chess.ROOK: 12, 
                chess.BISHOP: 13, 
                chess.KNIGHT: 14, 
                chess.PAWN: 15
            }
        }
        if position.is_capture(move):
            captured_piece = position.piece_at(move.to_square)
            capturing_piece = position.piece_at(move.from_square)
            if captured_piece is None:
                captured_piece = chess.Piece(piece_type=chess.PAWN, color=position.turn)
            return mvv_lva_table[captured_piece.piece_type][capturing_piece.piece_type]
        else:
            return 0

    legal_moves = list(position.legal_moves)
    return sorted(legal_moves, key=calc_move_value, reverse=True)

    
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
