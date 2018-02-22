import tkinter as tk
from tkinter import ttk

import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import math
from fileprocessing import read_file, read_ds_file
from data_handler import Data
matplotlib.use("TkAgg")
style.use('bmh')
# style.use('seaborn')


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Digital Signal Processing")
        master.geometry("800x600")

        self.master.protocol("WM_DELETE_WINDOW", self.master.quit)
        self.data = Data()
        self.scalar = 1
        self.popup_return = ''
        self.menubar = tk.Menu(self.master)
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.operations_menu = tk.Menu(self.menubar, tearoff=0)
        self.init_menubar()
        self.master.config(menu=self.menubar)
        self.path = ''
        self.fig = plt.figure(1)
        canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.plot_widget = canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.BOTTOM)

    def init_menubar(self):
        self.file_menu.add_command(label="Open", command=self.open_dialog)
        self.file_menu.add_command(
            label="Append", command=self.on_append)
        self.operations_menu.add_command(
            label="Add", command=self.on_add)
        self.operations_menu.add_command(
            label="Subtract", command=self.on_subtract)
        self.operations_menu.add_command(
            label="Scale", command=self.on_scale)
        self.operations_menu.add_command(
            label="Quantize", command=self.on_quantize)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Operations", menu=self.operations_menu)
        # self.filemenu.entryconfigure("Save", state=DISABLED)

    def open_dialog(self):
        self.path = tk.filedialog.askopenfilename()
        self.data.signals = [read_ds_file(self.path)]
        self.draw_on_canvas(clear=True)

    def on_append(self):
        self.path = tk.filedialog.askopenfilename()
        self.data.signals.append(read_ds_file(self.path))
        self.draw_on_canvas()

    def on_add(self):
        self.path = tk.filedialog.askopenfilename()
        self.data.apply_operation(read_ds_file(self.path), op='+')
        self.draw_on_canvas(clear=True)

    def on_subtract(self):
        self.path = tk.filedialog.askopenfilename()
        self.data.apply_operation(read_ds_file(self.path), op='-')
        self.draw_on_canvas(clear=True)

    def on_scale(self):
        self.popupmsg('Enter your value')
        self.data.apply_operation(self.scalar, op='s')
        self.draw_on_canvas(clear=True)

    def on_quantize(self):
        self.popupmsg('Number of Levels/Bits for example 3L/3B:')
        self.data.quantize(levels=self.scalar)
        self.draw_on_canvas(clear=True)

    def draw_on_canvas(self, clear=False):
        if clear:
            plt.clf()
        plt.gca().set_color_cycle(None)
        for signal in self.data.signals:
            # x_axis = range(len(signal))
            plt.scatter(signal.keys(), signal.values())
        self.fig.canvas.draw()

    def popupmsg(self, msg):
        popup = tk.Tk()
        popup.wm_title("")
        input = ttk.Entry(popup)

        def disable_event():
            pass
        popup.protocol("WM_DELETE_WINDOW", disable_event)

        def on_press():
            self.popup_return = input.get()
            if self.popup_return.endswith(('b', 'B')):
                self.scalar = int(math.pow(2, int(self.popup_return[:-1])))
            elif self.popup_return.endswith(('l', 'L')):
                self.scalar = int(self.popup_return[:-1])
            else:
                self.scalar = int(self.popup_return)
            popup.destroy()
            self.master.quit()

        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", padx=12)
        b = ttk.Button(popup, text="Submit", command=on_press)
        input.pack()
        b.pack(side='bottom')
        popup.mainloop()


root = tk.Tk()


gui = GUI(root)

root.mainloop()
