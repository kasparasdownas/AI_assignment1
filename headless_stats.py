import model
from ai import getNextBestMoveExpectiminimax
import multiprocessing as mp
from tqdm import tqdm
import time
import json
from datetime import datetime
from collections import Counter

def run_single_game(grid_size=4, search_depth=2):
    game_grid = model.Board(grid_size)  
    process_pool = mp.Pool(processes=4)
    highest_tile = 0
    
    try:
        while not game_grid.checkLoss():
            optimal_move = getNextBestMoveExpectiminimax(game_grid, process_pool, search_depth)
            game_grid.move(optimal_move)
            

            for row in game_grid.board:
                if row:  
                    highest_tile = max(highest_tile, max(row))
            
            for row in game_grid.board:  
                if 2048 in row:
                    return True, game_grid.score, highest_tile
    finally:
        process_pool.close()
        process_pool.terminate()
    
    return False, game_grid.score, highest_tile  

def run_statistics(num_games=50, grid_size=4, search_depth=2):

    successes = 0
    total_score = 0
    max_score = 0
    min_score = float('inf')
    scores = []
    highest_tiles = []
    highest_tile_counts = Counter()
    
    print(f"Running {num_games} games with AI (depth={search_depth})...")
    start_time = time.time()
    
    for game_num in range(num_games):
        won, score, highest_tile = run_single_game(grid_size, search_depth)
        result = "WIN" if won else "LOSS"
        print(f"Game {game_num+1}/{num_games}: {result} - Score: {score} - Highest Tile: {highest_tile}")
        
        if won:
            successes += 1
        total_score += score
        max_score = max(max_score, score)
        min_score = min(min_score, score)
        scores.append(score)
        highest_tiles.append(highest_tile)
        highest_tile_counts[highest_tile] += 1
    
    end_time = time.time()
    success_rate = (successes / num_games) * 100
    avg_score = total_score / num_games
    
    scores.sort()
    median_score = scores[len(scores)//2] if len(scores) % 2 == 1 else (scores[len(scores)//2 - 1] + scores[len(scores)//2]) / 2
    
    highest_tile_stats = {str(tile): count for tile, count in highest_tile_counts.items()}
    highest_tile_percentages = {str(tile): (count/num_games*100) for tile, count in highest_tile_counts.items()}
    
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
        'highest_tile_distribution': highest_tile_stats,
        'highest_tile_percentages': highest_tile_percentages,
        'total_time': end_time - start_time,
        'avg_time_per_game': (end_time - start_time) / num_games,
        'all_scores': scores,
        'all_highest_tiles': highest_tiles
    }
    
    filename = f'stats_depth{search_depth}_{num_games}games_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(results, f, indent=4)
    
    print(f"\nStatistics for depth={search_depth} ({num_games} games):")
    print(f"Total games played: {num_games}")
    print(f"Games won (reached 2048): {successes}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Average score: {avg_score:.2f}")
    print(f"Median score: {median_score}")
    print(f"Highest score: {max_score}")
    print(f"Lowest score: {min_score}")
    
    print("\nHighest Tile Distribution:")
    for tile, count in sorted(highest_tile_counts.items(), key=lambda x: x[0]):
        percentage = count / num_games * 100
        print(f"  {tile}: {count} games ({percentage:.1f}%)")
    
    print(f"\nTotal time: {end_time - start_time:.2f} seconds")
    print(f"Average time per game: {(end_time - start_time) / num_games:.2f} seconds")
    print(f"\nResults saved to: {filename}")
    
    return results

if __name__ == "__main__":
    run_statistics(100, search_depth=2)