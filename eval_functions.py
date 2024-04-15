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




    

