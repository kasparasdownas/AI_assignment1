import tkinter as tk
import random
import time
import json
import os
from ai import get_best_move  # Importing our AI

HIGH_SCORE_FILE = "highscore.json"

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.size = 4
        self.score = 0
        self.high_score = self.load_high_score()
        self.board = [[0] * self.size for _ in range(self.size)]
        self.tiles = []
        self.init_ui()
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()
        self.root.bind("<KeyPress>", self.handle_keypress)

    def load_high_score(self):
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r") as file:
                return json.load(file).get("high_score", 0)
        return 0

    def save_high_score(self):
        with open(HIGH_SCORE_FILE, "w") as file:
            json.dump({"high_score": self.high_score}, file)

    def init_ui(self):
        self.frame = tk.Frame(self.root, bg="gray")
        self.frame.grid()

        # Grid labels
        self.labels = [[tk.Label(self.frame, text="", width=6, height=3, font=("Arial", 24), relief="ridge") 
                        for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.labels[i][j].grid(row=i, column=j, padx=5, pady=5)

        # Score labels
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 18))
        self.score_label.grid()
        self.high_score_label = tk.Label(self.root, text=f"High Score: {self.high_score}", font=("Arial", 18))
        self.high_score_label.grid()

        # Buttons for AI mode
        self.ai_button = tk.Button(self.root, text="Play as AI", font=("Arial", 16), command=self.start_ai_play)
        self.ai_button.grid(pady=10)

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 4 if random.random() > 0.9 else 2

    def move(self, direction):
        def compress():
            new_board = [[0] * self.size for _ in range(self.size)]
            for i in range(self.size):
                pos = 0
                for j in range(self.size):
                    if self.board[i][j] != 0:
                        new_board[i][pos] = self.board[i][j]
                        pos += 1
            return new_board

        def merge():
            for i in range(self.size):
                for j in range(self.size - 1):
                    if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                        self.board[i][j] *= 2
                        self.score += self.board[i][j]
                        self.board[i][j + 1] = 0

        def reverse():
            for i in range(self.size):
                self.board[i].reverse()

        def transpose():
            self.board = [list(row) for row in zip(*self.board)]

        if direction == "left":
            self.board = compress()
            merge()
            self.board = compress()
        elif direction == "right":
            reverse()
            self.board = compress()
            merge()
            self.board = compress()
            reverse()
        elif direction == "up":
            transpose()
            self.board = compress()
            merge()
            self.board = compress()
            transpose()
        elif direction == "down":
            transpose()
            reverse()
            self.board = compress()
            merge()
            self.board = compress()
            reverse()
            transpose()

        self.animate_move()
        self.add_new_tile()
        self.update_ui()
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def animate_move(self):
        for i in range(self.size):
            for j in range(self.size):
                self.labels[i][j].after(50, self.update_ui)

    def update_ui(self):
        colors = {0: "#CDC1B4", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179", 16: "#F59563",
                  32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72", 256: "#EDCC61", 512: "#EDC850",
                  1024: "#EDC53F", 2048: "#EDC22E"}
        for i in range(self.size):
            for j in range(self.size):
                value = self.board[i][j]
                self.labels[i][j].config(text=str(value) if value != 0 else "", 
                                         bg=colors.get(value, "#3C3A32"), 
                                         fg="white" if value > 4 else "black")
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def handle_keypress(self, event):
        key_mapping = {"a": "left", "d": "right", "w": "up", "s": "down",
                       "Left": "left", "Right": "right", "Up": "up", "Down": "down"}
        if event.keysym in key_mapping:
            self.move(key_mapping[event.keysym])

    def is_game_over(self):
        """Check if any move is possible."""
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    return False  
                if j < self.size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False  
                if i < self.size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False  
        return True  

    def start_ai_play(self):
        """Starts AI play loop"""
        self.ai_button.config(state=tk.DISABLED)  # Disable button while AI plays
        self.ai_play()

    def ai_play(self):
        """AI plays automatically"""
        if self.is_game_over():
            self.ai_button.config(state=tk.NORMAL)  # Re-enable button
            return

        move = get_best_move(self.board, self.score, depth=5)
        if move is None:
            self.ai_button.config(state=tk.NORMAL)  
            return

        if move == "LEFT":
            self.move("left")
        elif move == "UP":
            self.move("up")
        elif move == "DOWN":
            self.move("down")
        elif move == "RIGHT":
            self.move("right")

        self.root.after(100, self.ai_play) # Call ai_play again after 100ms

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()