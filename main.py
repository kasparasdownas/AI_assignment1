from game import Game2048
from inputhandling import get_move

def main():
    game = Game2048()
    while True:
        game.print_board()
        move = get_move()
        if move == "Q":
            break
        if move in ['W', '\x1b[A']:
            game.move_up()
        elif move in ['S', '\x1b[B']:
            game.move_down()
        elif move in ['A', '\x1b[D']:
            game.move_left()
        elif move in ['D', '\x1b[C']:
            game.move_right()
        if game.is_game_over():
            game.print_board()
            print("Game Over!")
            break

if __name__ == "__main__":
    main()