import random
import chess

hashes = [[], [], [], []]
piece_order = ["R", "N", "B", "Q", "K", "P", "r", "n", "b", "q", "k", "p"]
transposition_table = {}

board = chess.Board()
    

def random_num():
    return random.randint(-9223372036854775808, 9223372036854775807)


def get_hash(position: chess.Board):
    hash_value = 0
    piece_map = position.piece_map()
    for square in piece_map.keys():
        hash_value ^= hashes[0][square][piece_order.index(piece_map[square].symbol())]

    if position.turn == chess.BLACK:
        hash_value ^= hashes[1][0]
    
    if position.has_kingside_castling_rights(chess.WHITE):
        hash_value ^= hashes[2][0]
    if position.has_queenside_castling_rights(chess.WHITE):
        hash_value ^= hashes[2][1]
    if position.has_kingside_castling_rights(chess.BLACK):
        hash_value ^= hashes[2][2]
    if position.has_queenside_castling_rights(chess.BLACK):
        hash_value ^= hashes[2][3]

    en_passant_square = position.ep_square
    if en_passant_square:
        hash_value ^= hashes[3][chess.square_file(position.ep_square)]
                                              
    return hash_value



def init_transposition_table():
    global hashes
    
    for _ in range(64):
        hashes[0].append([])
        for _ in range(12):
            hashes[0][-1].append(random_num())

    hashes[1].append(random_num())

    for _ in range(4):
        hashes[2].append(random_num())

    for _ in range(8):
        hashes[3].append(random_num())


def reset_transposition_table():
    global transposition_table
    transposition_table = {}


def search_transposition_table(position: chess.Board):
    position_hash = get_hash(position)
    return transposition_table.get(position_hash)


def store_transposition_table(position: chess.Board, value: dict):
    global transposition_table
    transposition_table[get_hash(position)] = value
