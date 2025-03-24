import model
import copy
import multiprocessing as mp

MAX_VALUE = 2**64
OPTIMAL_PATTERN = [[2,   2**2, 2**3, 2**4],
                [2**8, 2**7, 2**6, 2**5],
                [2**9, 2**10,2**11,2**12],
                [2**16,2**15,2**14,2**13]]

def calculate_pattern_score(game_grid):
    score = 0
    for i in range(game_grid.boardSize):
        for j in range(game_grid.boardSize):
            score += game_grid[i][j] * OPTIMAL_PATTERN[i][j]
    return score

def find_optimal_move(game_grid, process_pool, search_depth = 2):
    best_score = -MAX_VALUE
    best_move = model.movement_directions[0]
    results = []
    
    for direction in model.movement_directions:
        simulation_grid = copy.deepcopy(game_grid)
        points, valid_move = simulation_grid.move(direction, False)
        if not valid_move:
            continue
        results.append(process_pool.apply_async(expectimax_search, (simulation_grid, search_depth, direction)))

    results = [res.get() for res in results]

    for res in results:
        if res[0] >= best_score:
            best_score = res[0]
            best_move = res[1]

    return best_move

def expectimax_search(game_grid, search_depth, direction = None):
    if game_grid.check_game_over():
        return -MAX_VALUE, direction
    elif search_depth < 0:
        return calculate_pattern_score(game_grid), direction

    score = 0
    if search_depth != int(search_depth):
        # Player's turn, pick max
        score = -MAX_VALUE
        for direction in model.movement_directions:
            simulation_grid = copy.deepcopy(game_grid)
            points, moved = simulation_grid.move(direction, False)
            if moved:
                res = expectimax_search(simulation_grid, search_depth-0.5, direction)[0]
                if res > score: score = res
    elif search_depth == int(search_depth):
        # Nature's turn, calc average
        score = 0
        empty_cells = game_grid.get_empty_cells()
        for cell in empty_cells:
            game_grid.spawn_tile(cell, 2)
            score += 1.0/len(empty_cells)*expectimax_search(game_grid, search_depth - 0.5, direction)[0]
            game_grid.spawn_tile(cell, 0)
    return (score, direction)
