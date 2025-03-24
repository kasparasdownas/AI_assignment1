from random import random, choice
MOVE_LEFT = (0, -1)
MOVE_RIGHT = (0, 1)
MOVE_UP = (-1, 0)
MOVE_DOWN = (1, 0)
movement_directions = [MOVE_LEFT, MOVE_UP, MOVE_RIGHT, MOVE_DOWN]

class GameGrid:
    def __init__(self, grid_size = 4):
        self.boardSize = grid_size
        self.grid = [[0]*grid_size for i in range(grid_size)]
        self.total_score = 0
        self.spawn_tile()
        self.spawn_tile()

    def __str__(self):
        output = ''
        for row in self.grid:
            output += '\t'.join(map(str,row))
            output += '\n'
        return output

    def __getitem__(self, key):
        return self.grid[key]

    def get_empty_cells(self):
        empty_cells = []
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.grid[i][j] == 0:
                    empty_cells.append((i,j))
        return empty_cells

    def spawn_tile(self, position = None, value = 0):
        if position == None:
            empty_cells = self.get_empty_cells()
            if len(empty_cells) == 0:
                raise Exception("Unable to add tile, board is full")
            position = choice(empty_cells)

        if value == 0:
            if random() < 0.9:
                value = 2
            else:
                value = 4

        self.grid[position[0]][position[1]] = value

    def move(self, direction, spawn_new=True):
        collision_map = [[False]*self.boardSize for i in range(self.boardSize)]
        moved = False
        points = 0

        x_start = 0
        x_end = self.boardSize
        if direction[1] > 0:
            x_start = self.boardSize - 1
            x_end = -1

        y_start = 0
        y_end = self.boardSize
        if direction[0] > 0:
            y_start = self.boardSize - 1
            y_end = -1

        for y in range(y_start, y_end, -direction[0] if direction[0] != 0 else 1):
            for x in range(x_start, x_end, -direction[1] if direction[1] != 0 else 1):
                if self.grid[y][x] == 0:
                    continue

                y_check = y + direction[0]
                x_check = x + direction[1]

                while y_check >= 0 and y_check < self.boardSize \
                    and x_check >= 0 and x_check < self.boardSize \
                    and self.grid[y_check][x_check] == 0:
                    y_check += direction[0]
                    x_check += direction[1]

                if y_check < 0 or y_check >= self.boardSize \
                    or x_check < 0 or x_check >= self.boardSize:
                    y_check -= direction[0]
                    x_check -= direction[1]

                if y_check == y and x_check == x:
                    continue
                elif self.grid[y][x] == self.grid[y_check][x_check] and not collision_map[y_check][x_check]:
                    collision_map[y_check][x_check] = True
                    moved = True
                    self.grid[y_check][x_check] += self.grid[y][x]
                    points += self.grid[y_check][x_check]
                    self.grid[y][x] = 0
                elif self.grid[y_check][x_check] == 0:
                    moved = True
                    self.grid[y_check][x_check] = self.grid[y][x]
                    self.grid[y][x] = 0
                else:
                    y_check -= direction[0]
                    x_check -= direction[1]
                    if y_check == y and x_check == x:
                        continue
                    moved = True
                    temp = self.grid[y][x]
                    self.grid[y][x] = 0
                    self.grid[y_check][x_check] = temp

        self.total_score += points
        if moved and spawn_new:
            self.spawn_tile()
        return points, moved

    def check_game_over(self):
        for y in range(self.boardSize):
            for x in range(self.boardSize):
                if self.grid[y][x] == 0:
                    return False
                for direction in movement_directions:
                    if y + direction[0] >= 0 and y + direction[0] < self.boardSize \
                        and x + direction[1] >= 0 and x + direction[1] < self.boardSize \
                        and self.grid[y][x] == self.grid[y+direction[0]][x+direction[1]]:
                        return False
        return True
