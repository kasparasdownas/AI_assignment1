import time
from game import Game2048
from ai import get_best_move

def main():
    game = Game2048()
    while True:
        game.print_board()
        if game.is_game_over():
            break

        board_copy = [row[:] for row in game.board]
        score = game.score

        move = get_best_move(board_copy, score, depth=5)  
        if move is None:
            break

        print("AI selects move:", move)
        time.sleep(0.01)  

        if move == "UP":
            game.move_up()
        elif move == "DOWN":
            game.move_down()
        elif move == "LEFT":
            game.move_left()
        elif move == "RIGHT":
            game.move_right()

if __name__ == "__main__":
    main()