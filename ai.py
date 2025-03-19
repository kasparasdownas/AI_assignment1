import math

def clone_board(board):
    return [row[:] for row in board]

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

def boards_equal(b1, b2):
    size = len(b1)
    return all(b1[i][j] == b2[i][j] for i in range(size) for j in range(len(b1[0])))

def is_game_over_sim(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return False
            if j < size - 1 and board[i][j] == board[i][j+1]:
                return False
            if i < size - 1 and board[i][j] == board[i+1][j]:
                return False
    return True

def heuristic(board):
    free_cells = sum(cell == 0 for row in board for cell in row)
    max_tile = max(max(row) for row in board)
    return free_cells * 100 + max_tile

def expectimax(board, score, depth, is_player):
    if depth == 0 or is_game_over_sim(board):
        return heuristic(board)
    if is_player:
        best = -math.inf
        for move_func in [move_up_sim, move_down_sim, move_left_sim, move_right_sim]:
            new_board, new_score = move_func(board, score)
            if boards_equal(new_board, board):
                continue
            value = expectimax(new_board, new_score, depth - 1, False)
            best = max(best, value)
        return best if best != -math.inf else heuristic(board)
    else:
        total_value = 0
        empty_cells = [(i, j) for i in range(len(board))
                       for j in range(len(board[0])) if board[i][j] == 0]
        if not empty_cells:
            return heuristic(board)
        for i, j in empty_cells:
            for tile, prob in [(2, 0.9), (4, 0.1)]:
                new_board = clone_board(board)
                new_board[i][j] = tile
                value = expectimax(new_board, score, depth - 1, True)
                total_value += prob * value
        return total_value / len(empty_cells)

def get_best_move(board, score, depth=3):
    best_value = -math.inf
    best_move = None
    moves = {
        "UP": move_up_sim,
        "DOWN": move_down_sim,
        "LEFT": move_left_sim,
        "RIGHT": move_right_sim
    }
    for move_name, move_func in moves.items():
        new_board, new_score = move_func(board, score)
        if boards_equal(board, new_board):
            continue
        value = expectimax(new_board, new_score, depth, False)
        if value > best_value:
            best_value = value
            best_move = move_name
    return best_move