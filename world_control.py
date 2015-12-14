from world import World
from terrain import Terrain
from constance import *

class WorldControl:
    world_size = WORLD_SIZE         # world dimension
    cell_pixels = CELL_PIXELS       # pixels per cell

    def __init__(self, canvas):
        self.canvas = canvas
        self.world = World(WorldControl.world_size)
        #self.world.randomly_populate_cells()
        self.world.populate_cells()

    def draw(self):
        i=0
        for row in self.world:
            j=0
            for cell in row:
                # top left coords
                x0 = i * self.cell_pixels
                y0 = j * self.cell_pixels

                # bottom right coords
                x1 = (i+1)*self.cell_pixels
                y1 = (j+1)*self.cell_pixels

                cell.draw(self.canvas, x0, y0, x1, y1)
                cell.row = i
                cell.col = j
                j+=1
            i+=1
        self.canvas.pack()

    def step(self):
        self.world.step()
        self.draw()

    def get_steps(self):
        return self.world.steps

    def cell_at(self, x, y):
        return self.world.get_cell(int(x/self.cell_pixels), int(y/self.cell_pixels))

