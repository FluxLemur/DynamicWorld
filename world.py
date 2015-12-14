import random
import string
from sets import Set
from terrain import *
from actions import *
from animal import Animals
from PIL import Image, ImageTk

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
        self.photo = None

    def step(self):
        ''' change resources, step all animals in cell '''
        for animal in self.animals:
            action = animal.act()
            if type(action) is Move:
                self.move_animal(animal, action)
            elif type(action) == type(Sleep):
                pass

    def move_animal(self, animal, direction):
        d_row, d_col = Direction.get_tuple(direction)

    def contains_resource(self, r):
        return r in self.resources

    def animals_str(self):
        ret_str = ''
        for animal in self.animals:
            ret_str += type(animal).__name__ + ' '
        return ret_str

    def add_animal(self, animal):
        animal.cell = self
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
            name = animal.get_name().lower()
            original = Image.open(name + '.png')
            resized = original.resize((dx/2, dy/2),Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized)
            canvas.create_image(dx/2, dy/2, image= photo)
            self.photo = photo
            #canvas.create_rectangle(x0 + i*2, y0+5,x1+i*3, y1-5, fill=animal.color)
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
    def from_int(i, resources, animals, world, coord):
        terrain = Terrains.terrains[i]()
        # populate cell
        n = 0
        for resource in terrain.resources.iterkeys():
            terrain.resources[resource] = resources[n]
            n += 1
        cell = Cell(terrain, terrain.resources, world, coord)
        for a in animals:
            cell.add_animal(a)
        return cell

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
        f_world = open('world_config/world.txt', 'r')
        world = f_world.read().split()
        f_world.close()
        f_res = open('world_config/resources.txt', 'r')
        res = f_res.read().strip().split(' \n')
        f_res.close()
        f_anim = open('world_config/animals.txt', 'r')
        anim = f_anim.read().strip().split('\n')
        f_anim.close()
        i = 0
        for row in self.cells:
            for j in range(len(row)):
                resources = res[i].strip().split(' ')
                animal_i = int(anim[i])
                animals = []
                if animal_i != 0:
                    animals.append(Animals.animals[i-1](self))
                row[j] = Cell.from_int(int(world[i]), resources, animals, self, (row, j))
                i += 1

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