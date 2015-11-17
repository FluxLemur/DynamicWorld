from Tkinter import *
from display import Display

WIDTH = 500
HEIGHT = 500

class WorldControl:
    def __init__(self):
        self.master = Tk()
        self.master.title('World')
        self.master.bind("<Button-1>", self._click_callback)
        self.master.bind("<Key>", self._key_callback)

        self.canvas = Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack(side=TOP)
        self.stat_frame = Frame(self.master)
        self.stat_frame.pack(side=BOTTOM)
        self.display = Display(self.canvas)
        self._make_command_bar()
        self.popup = None

    def run(self):
        ''' Print display and start the Tkinter mainloop '''
        self.display.draw()
        mainloop()

    def _click_callback(self,event):
        cell = self.display.cell_at(event.x, event.y)
        self._cell_info_popup(cell)

    def _key_callback(self,event):
        press = repr(event.char)

        # ctrl-w and ctrl-q respectively
        if press == "'\\x17'" or press == "'\\x11'":
            self.master.quit()
        else:
            print press # TODO: remove this eventually

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
                             [('Loc:', loc), ('Terrain:', cell.terrain)])
        cell_info.pack(side=TOP)

        def key_callback(event):
            self.popup.destroy()
            self.popup = None

        self.popup.title(loc)
        self.popup.protocol("WM_DELETE_WINDOW", lambda : key_callback(None))
        self.popup.bind("<Key>", key_callback)

    def _make_command_bar(self):
        commands = Tk()
        commands.title('Commands')
        commands.bind("<Key>", self._key_callback)
        Button(commands, text='help', width=25).grid(row=0, column=0)
        Button(commands, text='play', width=25).grid(row=0, column=1)

if __name__ == '__main__':
    world = WorldControl()
    world.run()
