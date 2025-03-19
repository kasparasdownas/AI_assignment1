import random
import os

class Game2048:
    def __init__(self):
        self.size = 4
        self.cell_width = 7  
        self.score = 0
        self.board = [[0] * self.size for _ in range(self.size)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(self.size)
                       for j in range(self.size) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 4 if random.random() > 0.9 else 2

    def compress(self):
        new_board = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            pos = 0
            for j in range(self.size):
                if self.board[i][j] != 0:
                    new_board[i][pos] = self.board[i][j]
                    pos += 1
        self.board = new_board

    def merge(self):
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] != 0:
                    self.board[i][j] *= 2
                    self.score += self.board[i][j]
                    self.board[i][j + 1] = 0

    def reverse(self):
        for i in range(self.size):
            self.board[i] = self.board[i][::-1]

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_left(self):
        self.compress()
        self.merge()
        self.compress()
        self.add_new_tile()

    def move_right(self):
        self.reverse()
        self.move_left()
        self.reverse()

    def move_up(self):
        self.transpose()
        self.move_left()
        self.transpose()

    def move_down(self):
        self.transpose()
        self.move_right()
        self.transpose()

    def get_bg_color(self, value):
        bg_colors = {
            0: "\033[48;5;255m",   
            2: "\033[48;5;230m",
            4: "\033[48;5;229m",
            8: "\033[48;5;220m",
            16: "\033[48;5;214m",
            32: "\033[48;5;208m",
            64: "\033[48;5;202m",
            128: "\033[48;5;226m",
            256: "\033[48;5;190m",
            512: "\033[48;5;154m",
            1024: "\033[48;5;118m",
            2048: "\033[48;5;82m"
        }
        return bg_colors.get(value, "\033[48;5;250m")

    def get_fg_color(self, value):
        if value in (0, 2, 4, 8, 16):
            return "\033[30m"  #
        else:
            return "\033[97m"  

    def colored_tile(self, value):
        text = str(value) if value != 0 else ""
        text = text.center(self.cell_width)
        bg = self.get_bg_color(value)
        fg = self.get_fg_color(value)
        return f"{bg}{fg}{text}\033[0m"

    def print_separator(self):
        print("+" + ("-" * self.cell_width + "+") * self.size)

    def print_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"Score: {self.score}\n")
        self.print_separator()
        for row in self.board:
            row_str = "|".join(self.colored_tile(val) for val in row)
            print("|" + row_str + "|")
            self.print_separator()

    def is_game_over(self):
        for row in self.board:
            if 2048 in row:
                print("\033[32mYou win!\033[0m")
                return True
        if any(0 in row for row in self.board):
            return False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.board[i][j] == self.board[i + 1][j]:
                    return False
        print("\033[31mGame Over!\033[0m")
        return True