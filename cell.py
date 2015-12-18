from actions import *
from sets import Set
from terrain import *
from PIL import ImageTk
from resources import Resources as R
from collections import Counter
import math

class Cell:
    ''' A cell has a terrain and set of animals.
        This is equivalent to a NxN mile section of the simulated world, for
        some generalized N.'''
    def __init__(self, terrain, world, coord):
        self.terrain   = terrain
        self.animals   = Set()
        self.world     = world
        self.row, self.col = coord
        self.photo1 = None
        self.photo2 = None
        self.photo3 = None

    def step(self):
        ''' change resources, step all animals in cell '''
        self.terrain.step_resources()
        self.step_animals()

    def can_perform_action(self, action):
        ''' Returns True iff [action] can be performed '''
        if type(action) is Move:
            # only when the target cell is different is the move possible
            return self.get_relative_cell(action.direction) != self
        elif type(action) is Eat:
            if action.is_animal:
                return action.food in self.animals
            return self.terrain.contains(action.food)
        elif type(action) is Drink:
            return self.terrain.contains(R.water)
        elif type(action) is Mate:
            pass #TODO: handle

        else:
            assert type(action) is Sleep

            return True

    def step_animals(self):
        anim_to_remove = set() # dictionary cannot change size during iteration
                               # so we keep track of all the animals we have to
                               # remove at the end

        anim_to_move = {}      # mapping of animals : cell to be moved to
        anim_killed = set()    # keeps track of dead animals, so they're not moved

        new_animals = {}       # animals to be added, due to mating

        for animal in self.animals:
            if animal.last_step == self.world.steps:
                continue
            animal.last_step = self.world.steps

            action = animal.act()

            if animal.dead():
                print '{} on cell ({},{}) died of {}'.format(
                       animal.get_name(), self.col, self.row, animal.death_cause)
                anim_to_remove.add(animal)
                continue

            if type(action) is Move:
                to_cell = self.get_relative_cell(action.direction)
                if to_cell != self:
                    anim_to_remove.add(animal)
                    anim_to_move[animal] = to_cell

            elif type(action) is Drink:
                self.terrain.consume_resource(R.water)

            elif type(action) is Eat:
                if action.is_animal:
                    assert action.food in self.animals
                    action.food.be_eaten()
                    anim_to_remove.add(action.food)
                    anim_killed.add(action.food)
                else:
                    self.terrain.consume_resource(action.food)

            elif type(action) is Mate:
                partner = action.partner
                if (animal, partner) in new_animals or \
                   (partner, animal) in new_animals:
                       continue
                else:
                    child = Animal.birth_animal(animal, partner)
                    new_animals[(animal, partner)] = child

            elif type(action) is Sleep:
                pass

        for animal in anim_to_remove:
            self.animals.remove(animal)

        for animal,to_cell in anim_to_move.iteritems():
            if animal not in anim_killed:
                if to_cell:
                    to_cell.add_animal(animal)
        for animal in new_animals.itervalues():
            self.add_animal(animal)
            self.world.animals.add(animal)    # the world keeps track of all animals

    def get_animal_by_type(self, t):
        for a in self.animals:
            if type(a) is t:
                return a
        return None

    def get_relative_cell(self, direction):
        d_row, d_col = direction
        new_cell = self.world.get_relative_cell(self, d_row, d_col)
        return new_cell

    def contains_resource(self, r):
        return self.terrain.contains(r)

    def animals_str(self):
        ret_str = ''
        anim_strs = [str(animal) for animal in self.animals]
        return '\n'.join(anim_strs)

    def add_animal(self, animal):
        animal.current_cell = self
        animal.cells[self.row][self.col] = CellSnapshot(self, self.world.steps)
        self.animals.add(animal)

    def draw(self, canvas, x0, y0, x1, y1, use_images=True):
        ''' Draws this cell on a given canvas in an area defined by the rectangle
            (x0,y0), (x1,y1) '''
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.terrain.get_color(), outline='black')
        if self.terrain.no_resources():
            canvas.create_rectangle(x0, y0, x0+5, y0+5, fill='black')

        dx = x1-x0
        dy = y1-y0
        l = len(self.animals) * 5
        i = 1.0

        if use_images:
            in_cell = [False, False, False]       # (giraffe, tiger, elphant)
            for animal in self.animals:
                #print animal.get_name()
                if animal.get_name() == 'Giraffe':
                    in_cell[0] = True
                elif animal.get_name() == 'Tiger':
                    in_cell[1] = True
                else:
                    in_cell[2] = True

            g = in_cell[0]
            t = in_cell[1]
            e = in_cell[2]


            from animal import AnimalPhotos
            if g and t and e:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.giraffe[2])
                self.photo2 = ImageTk.PhotoImage(AnimalPhotos.elephant[2])
                self.photo3 = ImageTk.PhotoImage(AnimalPhotos.tiger[2])
                canvas.create_image(x0+dx/6, y0+dy/2, image = self.photo1)
                canvas.create_image(x0+dx/2, y0+dy/2, image = self.photo2)
                canvas.create_image(x0+5*dx/3, y0+dy/2, image = self.photo3)

            elif g and t:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.giraffe[1])
                self.photo2 = ImageTk.PhotoImage(AnimalPhotos.tiger[1])
                canvas.create_image(x0+dx/4, y0+dy/2, image = self.photo1)
                canvas.create_image(x0+3*dx/4, y0+dy/2, image = self.photo2)

            elif g and e:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.giraffe[1])
                self.photo2 = ImageTk.PhotoImage(AnimalPhotos.elephant[1])
                canvas.create_image(x0+dx/4, y0+dy/2, image = self.photo1)
                canvas.create_image(x0+3*dx/4, y0+dy/2, image = self.photo2)

            elif t and e:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.elephant[1])
                self.photo2 = ImageTk.PhotoImage(AnimalPhotos.tiger[1])
                canvas.create_image(x0+dx/4, y0+dy/2, image = self.photo1)
                canvas.create_image(x0+3*dx/4, y0+dy/2, image = self.photo2)

            elif g:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.giraffe[0])
                canvas.create_image(x0+dx/2, y0+dy/2, image = self.photo1)

            elif t:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.tiger[0])
                canvas.create_image(x0+dx/2, y0+dy/2, image = self.photo1)

            elif e:
                self.photo1 = ImageTk.PhotoImage(AnimalPhotos.elephant[0])
                canvas.create_image(x0+dx/2, y0+dy/2, image = self.photo1)

        else:
            for animal in self.animals:
                if use_images:
                    photo = ImageTk.PhotoImage(animal.photo)
                    canvas.create_image(x0+dx/2, y0+dy/2, image=photo)
                    self.photo = photo
                else:
                    canvas.create_rectangle(x0 + i*dx/l, y0+i*dy/l,x1-i*dx/l,
                        y1-i*dy/l,fill=animal.color)
                    i += 2

    def resources_str(self):
        return '[{}]'.format(
                '\n'.join(['{} {}'.format(v,k)
                    for k,v in self.terrain.resources.iteritems()]))

    @staticmethod
    def random_cell(world, coord):
        terrain = Terrains.random_terrain()
        return Cell(terrain, world, coord)

    @staticmethod
    def from_int(i, animals, world, coord):
        terrain = Terrains.terrains[i]()
        cell = Cell(terrain, world, coord)
        for a in animals:
            cell.add_animal(a)
        return cell

    def get_neighbors(self):
        # returns the neighbors of this cell in the world
        neighbors = set()

        for d_row, d_col in Direction.directions:
            new_cell = self.world.get_relative_cell(self, d_row, d_col)
            if new_cell != self:
                neighbors.add(new_cell)

        return neighbors

    @staticmethod
    def distance(cell1, cell2):
        dr = cell1.row - cell2.row
        dc = cell1.col - cell2.col

        dr *= dr
        dc *= dc

        return math.sqrt(dr + dc)

    @staticmethod
    def direction_to(from_cell, to_cell):
        # return the direction from one cell to another. If the cells have the
        # coordinates, then None
        assert from_cell is not None
        assert to_cell is not None
        dr = to_cell.row - from_cell.row
        dc = to_cell.col - from_cell.col

        if dr == 0 and dc == 0:
            return None

        ret = ()
        if abs(dr) > abs(dc):
            ret = (cmp(dr,0), 0)
        else:
            ret = (0, cmp(dc,0))
        return ret

class CellSnapshot():
    def __init__(self, cell, steps):
        self.row = cell.row
        self.col = cell.col
        self.animal_type_counter = Counter([type(a) for a in cell.animals])
        self.terrain_snapshot = TerrainSnapshot(cell.terrain)
        self.step_time = steps

    def has_food(self, foods):
        for food in foods:
            if type(food) in self.animal_type_counter:
                    return True
            elif self.terrain_snapshot.contains(food):
                return True
        return False

    def has_water(self):
        return self.terrain_snapshot.contains(R.water)
