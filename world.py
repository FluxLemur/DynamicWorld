import random
import string
from sets import Set
from terrain import *
from actions import *

class Cell:
    ''' A cell has a type of terrain, and sets of resources and animals.
        This is equivalent to a NxN mile section of the simulated world, for
        some generalized N.'''
    def __init__(self, terrain, resources, world, coord):
        self.terrain   = terrain
        self.resources = resources
        self.animals   = Set()
        self.world     = world
        self.row, self.col = coord

    def step(self):
        ''' change resources, step all animals in cell '''
        for animal in self.animals:
            action = animal.act()
            if type(action) is Move:
                self.move_animal(animal, action)
            elif type(action) == type(Actions.Sleep):
                kgt

    def move_animal(self, animal, direction):
        d_row, d_col = Direction.get_tuple(direction)

    def animals_str(self):
        ret_str = ''
        for animal in self.animals:
            ret_str += type(animal).__name__ + ' '
        return ret_str

    def add_animal(self, animal):
        self.animals.add(animal)

    def draw(self, canvas, x0, y0, x1, y1):
        ''' Draws this cell on a given canvas in an area defined by the rectangle
            (x0,y0), (x1,y1) '''
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.terrain.get_color(), outline='black')
        dx = x1-x0
        dy = y1-y0
        l = len(self.animals)
        i = 0
        for animal in self.animals:
            canvas.create_rectangle(x0 + i*2, y0+5,x1+i*3, y1-5, fill=animal.color)
            i += 1

    def resources_str(self):
        return '[{}]'.format(
                    '\n'.join(['{} {}'.format(v,k) for k,v in self.resources.iteritems()])
                    )

    @staticmethod
    def random_cell(world, coord):
        terrain = Terrains.random_terrain()
        return Cell(terrain, terrain.resources, world, coord)

    @staticmethod
    def from_int(i, resources, world, coord):
        terrain = Terrains.terrains[i]()

        # populate cell
        n = 0
        for resource in terrain.resources.iterkeys():
            terrain.resources[resource] = resources[n]
            n += 1
        return Cell(terrain, terrain.resources, world, coord)

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
                row[j] = Cell.random_cell(self, (row, j))

    def populate_cells(self):
        f = open('world_config/world.txt', 'r')
        s = f.read()
        s = s.split()
        f.close()
        f = open('world_config/resources.txt', 'r')
        r = f.read()
        r = r.split(' \n')
        r = r[0:100]
        i = 0
        for row in self.cells:
            for j in range(len(row)):
                resources = r[i].strip().split(' ')
                row[j] = Cell.from_int(int(s[i]), resources, self, (row, j))
                i += 1
        f.close()

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
