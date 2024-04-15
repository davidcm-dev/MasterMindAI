import chess

killer_moves: dict[int, list] = {}


def add_killer_move(move: chess.Move, ply: int):
    global killer_moves
    if ply in killer_moves:
        current_killers = killer_moves[ply]
        if len(current_killers) < 2 and move not in current_killers:
            killer_moves[ply].insert(0, move)
        else:
            if move not in current_killers:
                killer_moves[ply].pop()
                killer_moves[ply].insert(0, move)
    else:
        killer_moves[ply] = [move]
    


def order_mvv_lva(position: chess.Board, legal_moves: list):
    num_captures = 0
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
            nonlocal num_captures
            num_captures += 1
            captured_piece = position.piece_at(move.to_square)
            capturing_piece = position.piece_at(move.from_square)
            if captured_piece is None:
                captured_piece = chess.Piece(piece_type=chess.PAWN, color=position.turn)
            return mvv_lva_table[captured_piece.piece_type][capturing_piece.piece_type]
        else:
            return 0
    
    return [sorted(legal_moves, key=calc_move_value, reverse=True), num_captures]


def order_killer_moves(position: chess.Board, mvv_lva_list: list[chess.Move], num_ordered_moves: int):
    ordered_moves = mvv_lva_list[:num_ordered_moves]
    unordered_moves = mvv_lva_list[num_ordered_moves:]
    for move in unordered_moves:
        try:
            if move in killer_moves[position.ply()]:
                unordered_moves.remove(move)
                unordered_moves.insert(0, move)
        except KeyError:
            pass
    return ordered_moves + unordered_moves


def order_moves(position: chess.Board):
    legal_moves = list(position.pseudo_legal_moves)
    mvv_lva_list, num_ordered_moves = order_mvv_lva(position,legal_moves)
    return order_killer_moves(position, mvv_lva_list, num_ordered_moves)
