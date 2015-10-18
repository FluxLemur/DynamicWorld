from world import World

class Display:
    world_size = (10,10)  # world dimension
    cell_pixels = 50        # cell_pixelsels per cell

    # for colors, see http://wiki.tcl.tk/37701
    terrain_colors = {'Plains':'spring green', 'Forest':'forest green', \
                   'Desert':'dark khaki', 'Mountain':'slate grey'}

    def __init__(self, canvas):
        self.world = World(Display.world_size)
        self.canvas = canvas

    def draw(self):
        i=0
        for row in self.world:
            j=0
            for cell in row:
                color = self.terrain_colors[cell.terrain]

                # top left coords
                x0 = i * self.cell_pixels
                y0 = j * self.cell_pixels

                # bottom right coords
                x1 = (i+1)*self.cell_pixels
                y1 = (j+1)*self.cell_pixels

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
                cell.row = i
                cell.col = j
                j+=1
            i+=1
        self.canvas.pack()

    def cell_at(self, x, y):
        return self.world.get_cell(int(x/self.cell_pixels), int(y/self.cell_pixels))

