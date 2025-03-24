import sys, pygame
import model
from math import log2
from ai import *
import multiprocessing as mp
is_ai_enabled = False
search_depth = 2

# UI
window_dimensions = width, height = 600, 700
game_area = 600, 600
FPS = 60

# Colors
background_color = (187, 173, 160)  # Light gray background
text_color = (119, 110, 101)  # Dark gray text
text_color_light = (249, 246, 242)  # Light text for dark tiles
tile_base_color = (205, 193, 180)  # Empty tile color
tile_border_color = (187, 173, 160)  # Border color

# Tile colors based on value
tile_colors = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Game
grid_size = 4
grid_padding = 15
tile_radius = 6  # Rounded corners radius

def draw_rounded_rect(surface, color, rect, radius):
    """Draw a rectangle with rounded corners"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def render_game_state(display, game_board):
    # Draw background
    display.fill(background_color)
    
    # Draw game area background
    game_area_rect = pygame.Rect(0, 0, game_area[0], game_area[1])
    draw_rounded_rect(display, (205, 193, 180), game_area_rect, 6)
    
    # Draw tiles
    for i in range(game_board.boardSize):
        for j in range(game_board.boardSize):
            # Calculate tile position with padding
            tile_x = j * (game_area[0] - 2 * grid_padding) / game_board.boardSize + grid_padding
            tile_y = i * (game_area[1] - 2 * grid_padding) / game_board.boardSize + grid_padding
            tile_width = (game_area[0] - 2 * grid_padding) / game_board.boardSize - grid_padding
            tile_height = (game_area[1] - 2 * grid_padding) / game_board.boardSize - grid_padding
            
            tile_rect = pygame.Rect(tile_x, tile_y, tile_width, tile_height)
            
            # Draw tile
            value = game_board.grid[i][j]
            if value != 0:
                # Get color based on value
                color = tile_colors.get(value, (237, 194, 46))  # Default to 2048 color for higher values
                draw_rounded_rect(display, color, tile_rect, tile_radius)
                
                # Draw value text
                value_text = str(value)
                font_size = int(min(tile_width, tile_height) * 0.6)
                number_font = pygame.font.SysFont("Arial", font_size, bold=True)
                text_color = text_color_light if value in [2, 4] else text_color_light
                
                text_surface = number_font.render(value_text, True, text_color)
                text_rect = text_surface.get_rect(center=tile_rect.center)
                display.blit(text_surface, text_rect)
            else:
                draw_rounded_rect(display, tile_base_color, tile_rect, tile_radius)
    
    # Draw score panel
    score_panel = pygame.Rect(0, game_area[1], game_area[0], 100)
    draw_rounded_rect(display, (205, 193, 180), score_panel, 6)
    
    # Score text
    score_text = f"Score: {game_board.total_score:,}"
    score_font = pygame.font.SysFont("Arial", 36, bold=True)
    score_surface = score_font.render(score_text, True, text_color)
    score_rect = score_surface.get_rect(center=(game_area[0]/2, game_area[1] + 30))
    display.blit(score_surface, score_rect)
    
    # AI status
    ai_text = f"AI: {'Enabled' if is_ai_enabled else 'Disabled'} (Depth: {search_depth})"
    ai_font = pygame.font.SysFont("Arial", 24)
    ai_surface = ai_font.render(ai_text, True, text_color)
    ai_rect = ai_surface.get_rect(center=(game_area[0]/2, game_area[1] + 70))
    display.blit(ai_surface, ai_rect)
    
    # Controls hint
    controls_text = "Controls: Arrow keys to move, SPACE to toggle AI, R to reset, ESC to quit"
    controls_font = pygame.font.SysFont("Arial", 16)
    controls_surface = controls_font.render(controls_text, True, text_color)
    controls_rect = controls_surface.get_rect(center=(game_area[0]/2, game_area[1] + 90))
    display.blit(controls_surface, controls_rect)

def process_input(event, game_board):
    global is_ai_enabled, search_depth

    if event.type == pygame.QUIT:
        process_pool.close()
        process_pool.terminate()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            game_board.move(model.MOVE_RIGHT)
        elif event.key == pygame.K_LEFT:
            game_board.move(model.MOVE_LEFT)
        elif event.key == pygame.K_UP:
            game_board.move(model.MOVE_UP)
        elif event.key == pygame.K_DOWN:
            game_board.move(model.MOVE_DOWN)
        if event.key == pygame.K_r:
            game_board = model.GameGrid(grid_size)
        elif event.key == pygame.K_ESCAPE:
            process_pool.close()
            process_pool.terminate()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            is_ai_enabled = not is_ai_enabled
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
            search_depth = min(search_depth + 1, 4)
        elif event.key == pygame.K_MINUS:
            search_depth = max(search_depth - 1, 1)

    return game_board

def main_game_loop():
    global search_depth
    game_clock = pygame.time.Clock()
    game_board = model.GameGrid(grid_size)

    while 1:
        for event in pygame.event.get():
            game_board = process_input(event, game_board)

        if is_ai_enabled and not game_board.check_game_over():
            optimal_move = find_optimal_move(game_board, process_pool, search_depth)
            game_board.move(optimal_move)

        render_game_state(game_display, game_board)
        pygame.display.flip()
        game_clock.tick(FPS)

if __name__ == '__main__':
    global game_display
    global process_pool
    mp.freeze_support()
    mp.set_start_method('spawn')
    process_pool = mp.Pool(processes=4)

    pygame.init()
    game_display = pygame.display.set_mode(window_dimensions)
    pygame.display.set_caption("2048")
    main_game_loop()
