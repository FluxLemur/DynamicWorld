from Tkinter import *
from world_control import WorldControl

WIDTH = 500
HEIGHT = 500

class ControlHub:
    def __init__(self):
        self.master = Tk()
        self.master.title('World')
        self.master.bind("<Button-1>", self._click_callback)
        self.master.bind("<Key>", self._key_callback)

        self.canvas = Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=TOP)
        self.world_control = WorldControl(self.canvas)
        self._make_command_bar()
        self.popup = None

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
        else:
            print press # TODO: remove this eventually
            pass

    def _cell_info_popup(self, cell):
        if self.popup:
            self.popup.destroy()
        self.popup = Tk()

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
        cell_info = TileInfo(self.popup,
                    [('Loc:', loc), ('Terrain:', cell.terrain), ('Resources:', \
                            cell.resources_str()), ('Animals:', cell.animals_str())])
        cell_info.pack(side=TOP)

        def key_callback(event):
            self.popup.destroy()
            self.popup = None

        self.popup.title(loc)
        self.popup.protocol("WM_DELETE_WINDOW", lambda : key_callback(None))
        self.popup.bind("<Key>", key_callback)

    def step(self):
        self.world_control.step()
        print self.world_control.get_steps()
        #print step_str.get()

        # for some reason this doesn't work
        #step_str.set(str(self.world_control.get_steps()))

    def _make_command_bar(self):
        #step_str = StringVar(self.master)
        #step_str.set('0')
        def _help():
            pass
        def _play():
            pass
        def _step():
            self.step()

        commands = Tk()
        commands.title('Commands')
        commands.bind("<Key>", self._key_callback)
        Button(commands, text='help', width=15, command=_help).grid(row=0, column=0)
        Button(commands, text='play', width=15, command=_play).grid(row=0, column=1)
        Button(commands, text='step', width=15, command=_step).grid(row=0, column=2)

if __name__ == '__main__':
    world = ControlHub()
    world.run()
