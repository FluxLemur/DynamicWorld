from Tkinter import *
from world_control import WorldControl
from constance import *

WIDTH  = CELL_PIXELS * WORLD_SIZE[0]
HEIGHT = CELL_PIXELS * WORLD_SIZE[1]
N_STEPS = 100

class ControlHub:
    def __init__(self, use_images):
        self.master = Tk()
        self.master.title('World')
        self.master.bind("<Button-1>", self._click_callback)
        self.master.bind("<Key>", self._key_callback)

        self.canvas = Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=TOP)
        self.world_control = WorldControl(self.canvas, use_images)
        self._make_command_bar()
        self.info_popup = None    # TODO: does this as a mouseover???

    def run(self):
        ''' Print world_control and start the Tkinter mainloop '''
        self.world_control.draw()
        mainloop()

    def _click_callback(self,event):
        cell = self.world_control.cell_at(event.x, event.y)
        self._cell_info_popup(cell)

    def _key_callback(self,event):
        press = repr(event.char)

        # ctrl-w and ctrl-q respectively
        if press == "'\\x17'" or press == "'\\x11'":
            self.master.quit()
        elif press == "'\\r'" or press == "' '":
            self.step()
        elif press == "'\\\\'":
            self.step_many()
        elif press == "']'":
            self.step_until_done()
        else:
            print press # TODO: remove this eventually

    def _cell_info_popup(self, cell):
        if self.info_popup:
            self.info_popup.destroy()
        self.info_popup = Tk()

        class TileInfo(Frame):
            ''' This class simply governs the popup when you press on a tile '''
            def __init__(self,parent,info_text_pairs):
                Frame.__init__(self, parent)
                # forces the info window to not be too small
                parent.minsize(width=110,height=40)
                rowi = 0
                for (info,text) in info_text_pairs:
                    Label(self, text=info).grid(row=rowi, column=0)
                    Label(self, text=text).grid(row=rowi, column=1)
                    rowi += 1

        loc = str(cell.row) + ', ' + str(cell.col)

        # Tile information
        cell_info = TileInfo(self.info_popup,
                    [('Loc:', loc), ('Terrain:', cell.terrain), ('Resources:', \
                            cell.resources_str()), ('Animals:', cell.animals_str())])
        cell_info.pack(side=TOP)

        def key_callback(event):
            if event and repr(event.char) == "'\\x1b'" or event is None:
                self.info_popup.destroy()
                self.info_popup = None

        self.info_popup.title(loc)
        self.info_popup.protocol("WM_DELETE_WINDOW", lambda : key_callback(None))
        self.info_popup.bind("<Key>", key_callback)

    def step(self, draw=True):
        self.world_control.step(draw=draw)
        print self.world_control.get_steps()
        #print step_str.get()

        # for some reason this doesn't work
        #step_str.set(str(self.world_control.get_steps()))


    def step_many(self):
        for i in xrange(N_STEPS-1):
            self.world_control.step(draw=False)
        self.step()

    def step_until_done(self):
        while not self.world_control.done:
            self.step(False)

    def _make_command_bar(self):
        #step_str = StringVar(self.master)
        #step_str.set('0')
        def _step():
            self.step()
        def _step_many():
            self.step_many()

        def _step_until_done():
            self.step_until_done()

        commands = Tk()
        commands.title('Commands')
        commands.bind("<Key>", self._key_callback)
        Button(commands, text='step', width=15, command=_step).grid(row=0, column=0)
        Button(commands, text='step 100', width=15, command=_step_many).grid(row=0, column=1)
        Button(commands, text='step until done', width=15,
               command=_step_until_done).grid(row=0, column=2)

def main():
    use_images = True
    if len(sys.argv) >= 2 and sys.argv[1] in ['--no_images', '-n']:
        use_images = False
    world = ControlHub(use_images)
    world.run()

if __name__ == '__main__':
    main()
