import random

terrains = ['Plains', 'Forest', 'Desert', 'Mountain']

def random_terrain():
    return random.choice(terrains)

class Cell:
    def __init__(self, terrain):
        self.terrain = terrain
        self.row = 0
        self.col = 0

class World:
    def __init__(self, size):
        self.cells = [[Cell(random_terrain()) for x in range(size[0])] for x in range(size[1])]
        self.current = 0
        self.high = size[1]

    def __iter__(self):
        return self

    def next(self):
        if self.current >= self.high:
            self.current = 0
            raise StopIteration
        self.current += 1
        return self.cells[self.current-1]

    def set_cell(self, x, y, cell):
        self.cells[x][y] = cell

    def get_cell(self, x, y):
        return self.cells[x][y]
