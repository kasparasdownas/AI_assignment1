import model
from ai import find_optimal_move
import multiprocessing as mp
from tqdm import tqdm
import time
import json
from datetime import datetime

def run_single_game(grid_size=4, search_depth=2):
    """Run a single game with AI and return whether it reached 2048"""
    game_grid = model.GameGrid(grid_size)
    process_pool = mp.Pool(processes=4)
    
    try:
        while not game_grid.check_game_over():
            optimal_move = find_optimal_move(game_grid, process_pool, search_depth)
            game_grid.move(optimal_move)
            
            # Check if we reached 2048
            for row in game_grid.grid:
                if 2048 in row:
                    return True, game_grid.total_score
    finally:
        process_pool.close()
        process_pool.terminate()
    
    return False, game_grid.total_score

def run_statistics(num_games=100, grid_size=4, search_depth=2):
    """Run multiple games and calculate statistics"""
    successes = 0
    total_score = 0
    max_score = 0
    min_score = float('inf')
    scores = []
    
    print(f"Running {num_games} games with AI (depth={search_depth})...")
    start_time = time.time()
    
    for game_num in tqdm(range(num_games)):
        won, score = run_single_game(grid_size, search_depth)
        if won:
            successes += 1
        total_score += score
        max_score = max(max_score, score)
        min_score = min(min_score, score)
        scores.append(score)
    
    end_time = time.time()
    success_rate = (successes / num_games) * 100
    avg_score = total_score / num_games
    
    # Calculate median score
    scores.sort()
    median_score = scores[len(scores)//2] if len(scores) % 2 == 0 else scores[len(scores)//2]
    
    # Save results to a JSON file
    results = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'num_games': num_games,
        'grid_size': grid_size,
        'search_depth': search_depth,
        'success_rate': success_rate,
        'avg_score': avg_score,
        'median_score': median_score,
        'max_score': max_score,
        'min_score': min_score,
        'total_time': end_time - start_time,
        'avg_time_per_game': (end_time - start_time) / num_games,
        'all_scores': scores
    }
    
    filename = f'stats_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\nStatistics:")
    print(f"Total games played: {num_games}")
    print(f"Games won (reached 2048): {successes}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average score: {avg_score:.2f}")
    print(f"Median score: {median_score}")
    print(f"Highest score: {max_score}")
    print(f"Lowest score: {min_score}")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Average time per game: {(end_time - start_time) / num_games:.2f} seconds")
    print(f"\nResults saved to: {filename}")
    
    return results

if __name__ == "__main__":
    # Run 100 games with default settings (4x4 grid, depth=2)
    run_statistics(100) 