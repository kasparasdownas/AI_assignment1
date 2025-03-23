import time
import json
import tkinter as tk
from game import Game2048
from ai import get_best_move

HIGH_SCORE_FILE = "highscore.json"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return json.load(file).get("highscore", 0)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            json.dump({"highscore": score}, file)
        print(f"🎉 New High Score: {score}!")

def ai_play(game):
    """Let the AI play automatically"""
    if game.is_game_over():
        save_high_score(game.score)
        print("💀 Game Over!")
        return

    move = get_best_move(game.board, game.score, depth=5)
    if move is None:
        save_high_score(game.score)
        print("❌ No valid moves left!")
        return

    if move == "UP":
        game.move_up()
    elif move == "DOWN":
        game.move_down()
    elif move == "LEFT":
        game.move_left()
    elif move == "RIGHT":
        game.move_right()

    game.update_idletasks()
    game.after(100, lambda: ai_play(game))

def main():
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

if __name__ == "__main__":
    main()