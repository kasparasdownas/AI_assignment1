import math
import random
import copy

memo = {}

def clone_board(board):
    return copy.deepcopy(board)

def compress_board(board):
    size = len(board)
    new_board = [[0] * size for _ in range(size)]
    for i in range(size):
        pos = 0
        for j in range(size):
            if board[i][j] != 0:
                new_board[i][pos] = board[i][j]
                pos += 1
    return new_board

def merge_board(board, score):
    size = len(board)
    for i in range(size):
        for j in range(size - 1):
            if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                board[i][j] *= 2
                score += board[i][j]
                board[i][j + 1] = 0
    return board, score

def move_left_sim(board, score):
    new_board = compress_board(board)
    new_board, new_score = merge_board(new_board, score)
    new_board = compress_board(new_board)
    return new_board, new_score

def reverse_board(board):
    return [row[::-1] for row in board]

def move_right_sim(board, score):
    rev_board = reverse_board(board)
    new_board, new_score = move_left_sim(rev_board, score)
    new_board = reverse_board(new_board)
    return new_board, new_score

def transpose_board(board):
    return [list(row) for row in zip(*board)]

def move_up_sim(board, score):
    trans_board = transpose_board(board)
    new_board, new_score = move_left_sim(trans_board, score)
    new_board = transpose_board(new_board)
    return new_board, new_score

def move_down_sim(board, score):
    trans_board = transpose_board(board)
    new_board, new_score = move_right_sim(trans_board, score)
    new_board = transpose_board(new_board)
    return new_board, new_score

def is_game_over_sim(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return False
            if j < size - 1 and board[i][j] == board[i][j + 1]:
                return False
            if i < size - 1 and board[i][j] == board[i + 1][j]:
                return False
    return True

def heuristic(board):
    """Simple heuristic that prioritizes moving numbers left and having higher numbers on top."""
    free_cells = sum(cell == 0 for row in board for cell in row)
    max_tile = max(max(row) for row in board)
    
    # Score board positioning: prefer higher numbers on top and more free cells
    row_priority = sum(board[i][j] * (4 - j) for i in range(4) for j in range(4))
    
    return free_cells * 1000 + row_priority + max_tile

def get_best_move(board, score, depth=2):
    """AI only moves in one of the 4 directions and chooses the best move based on heuristic."""
    best_value = -math.inf
    best_move = None
    moves = {
        "LEFT": move_left_sim,  
        "UP": move_up_sim,
        "DOWN": move_down_sim,
        "RIGHT": move_right_sim  
    }
    
    for move_name, move_func in moves.items():
        new_board, new_score = move_func(board, score)
        if new_board == board:
            continue
        value = heuristic(new_board)
        if value > best_value:
            best_value = value
            best_move = move_name
    
    return best_move