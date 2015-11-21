import random
import string
from sets import Set
from terrain import Terrains
from actions import Actions

class Cell:
    ''' A cell has a type of terrain, and sets of resources and animals.
        This is equivalent to a NxN mile section of the simulated world, for
        some generalized N.'''
    def __init__(self, terrain, resources):
        self.terrain   = terrain
        self.resources = resources
        self.animals   = Set()
        self.x = -1
        self.y = -1

    def step(self):
        ''' change resources, step all animals in cell '''
        for animal in self.animals:
            action = animal.act()

    def add_animal(self, animal):
        self.animals.add(animal)

    def draw(self, canvas, x0, y0, x1, y1):
        ''' Draws this cell on a given canvas in an area defined by the rectangle
            (x0,y0), (x1,y1) '''
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.terrain.get_color(), outline='black')

    def resources_str(self):
        return '[{}]'.format(
                    '\n'.join(['{} {}'.format(v,k) for k,v in self.resources.iteritems()])
                    )

    @staticmethod
    def random_cell():
        terrain = Terrains.random_terrain()
        return Cell(terrain, terrain.resources)

class World:
    def __init__(self, size):
        ''' [size]: (height, width) '''
        self.cells = [[None for x in range(size[1])] for x in range(size[0])]
        self.current = 0
        self.high = size[1]
        self.steps = 0

    def __iter__(self):
        return self

    def step(self):
        ''' do one time step in the world '''
        for row in self.cells:
            for cell in row:
                cell.step()
        self.steps += 1

    def randomly_populate_cells(self):
        for row in self.cells:
            for j in range(len(row)):
                row[j] = Cell.random_cell()

    def next(self):
        if self.current >= self.high:
            self.current = 0
            raise StopIteration
        self.current += 1
        return self.cells[self.current-1]

    def set_cell(self, x, y, cell):
        cell.x = x
        cell.y = y
        self.cells[x][y] = cell

    def get_cell(self, x, y):
        return self.cells[x][y]

    def add_animal(self, x, y, animal):
        self.cells[x][y].add_animal(animal)
