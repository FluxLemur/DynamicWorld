from actions import *
from sets import Set
from terrain import *
from PIL import ImageTk

class Cell:
    ''' A cell has a terrain and set of animals.
        This is equivalent to a NxN mile section of the simulated world, for
        some generalized N.'''
    def __init__(self, terrain, world, coord):
        self.terrain   = terrain
        self.animals   = Set()
        self.world     = world
        self.row, self.col = coord
        self.photo = None

    def step(self):
        ''' change resources, step all animals in cell '''
        self.terrain.step_resources()
        self.step_animals()

    def step_animals(self):
        anim_to_remove = [] # dictionary cannot change size during iteration
                            # so we keep track of all the animals we have to
                            # remove at the end
        for animal in self.animals:
            action = animal.act()
            if type(action) is Move or type(action) is RandomMove:
                anim = self.move_animal(animal, action.direction)
                if anim:
                    anim_to_remove.append(anim)
            elif type(action) is Drink:

                pass
            elif type(action) is Eat:
                pass
            elif type(action) is Sleep:
                pass

        for anim in anim_to_remove:
            self.animals.remove(anim)


    def move_animal(self, animal, direction):
        assert (animal in self.animals)
        d_row, d_col = Direction.get_tuple(direction)
        new_cell = self.world.get_relative_cell(self, d_row, d_col)

        if new_cell != self:
            new_cell.add_animal(animal)
            return animal
        return None

    def contains_resource(self, r):
        return r in self.terrain.resources

    def animals_str(self):
        ret_str = ''
        for animal in self.animals:
            ret_str += type(animal).__name__ + ' '
        return ret_str

    def add_animal(self, animal):
        animal.cell = self
        self.animals.add(animal)

    def draw(self, canvas, x0, y0, x1, y1, use_images=True):
        ''' Draws this cell on a given canvas in an area defined by the rectangle
            (x0,y0), (x1,y1) '''
        canvas.create_rectangle(x0, y0, x1, y1, fill=self.terrain.get_color(), outline='black')
        dx = x1-x0
        dy = y1-y0
        l = len(self.animals) * 5
        i = 1.0
        for animal in self.animals:
            if use_images:
                photo = ImageTk.PhotoImage(animal.photo)
                canvas.create_image(x0+dx/2, y0+dy/2, image=photo)
                self.photo = photo
            else:
                canvas.create_rectangle(x0 + i*dx/l, y0+i*dy/l,x1-i*dx/l, y1-i*dy/l,
                                        fill=animal.color)
                i += 2

    def resources_str(self):
        return '[{}]'.format(
                '\n'.join(['{} {}'.format(v,k)
                    for k,v in self.terrain.resources.iteritems()])
                )

    @staticmethod
    def random_cell(world, coord):
        terrain = Terrains.random_terrain()
        return Cell(terrain, world, coord)

    @staticmethod
    def from_int(i, resources, animals, world, coord):
        terrain = Terrains.terrains[i]()
        # populate cell
        n = 0
        for r, resource in terrain.resources.iteritems():
            terrain.resources[r] = int(resources[n])
            n += 1
        cell = Cell(terrain, world, coord)
        for a in animals:
            cell.add_animal(a)
        return cell
