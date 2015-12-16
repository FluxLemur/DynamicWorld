from world import World
from terrain import Terrain
from constance import *

class WorldControl:
    world_size = WORLD_SIZE         # world dimension
    cell_pixels = CELL_PIXELS       # pixels per cell

    def __init__(self, canvas, use_images=True):
        self.canvas = canvas
        self.world = World(WorldControl.world_size)
        #self.world.randomly_populate_cells()
        self.world.populate_cells()
        self.use_images = use_images
        self.done = False

    def draw(self):
        self.canvas.delete('all')
        i=0
        for row in self.world.cells:
            j=0
            for cell in row:
                # top left coords
                x0 = j * self.cell_pixels
                y0 = i * self.cell_pixels

                # bottom right coords
                x1 = (j+1)*self.cell_pixels
                y1 = (i+1)*self.cell_pixels

                cell.draw(self.canvas, x0, y0, x1, y1, self.use_images)
                j+=1
            i+=1
        self.canvas.pack()

    def step(self, draw=True):
        if self.done:
            return

        self.world.step()
        if draw:
            self.draw()

        if self.world.all_dead():
            self.world.print_animal_stats()
            self.done = True
            self.draw()
            return

    def get_steps(self):
        return self.world.steps

    def cell_at(self, x, y):
        return self.world.get_cell(int(y/self.cell_pixels), int(x/self.cell_pixels))
