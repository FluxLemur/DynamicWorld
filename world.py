import random
from sets import Set
from terrain import Terrain

class Cell:
    ''' A cell has a type of terrain, and sets of resources and animals.
        This is equivalent to a NxN mile section of the simulated world, for
        some generalized N.'''
    def __init__(self, terrain, resources):
        self.terrain = terrain
        self.resources = resources
        self.animals = Set()
        self.row = 0
        self.col = 0

class World:
    def __init__(self, size):
        ''' [size]: (height, width) '''
        self.cells = [[None for x in range(size[1])] for x in range(size[0])]
        self.current = 0
        self.high = size[1]
        self.terrain = Terrain()

    def __iter__(self):
        return self

    def randomly_populate_cells(self):
        for i in self.cells:
            for j in range(len(i)):
                terrain = self.terrain.random_terrain()
                i[j] = Cell(terrain[0], terrain[1])

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
