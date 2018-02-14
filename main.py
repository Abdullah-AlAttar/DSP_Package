from tkinter import Tk, Menu, Entry, Label, NORMAL, DISABLED, E, W, filedialog, END, BOTTOM, CENTER

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

from fileprocessing import read_file


class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Digital Signal Processing")
        master.geometry("800x600")

        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.init_filemenu()
        self.master.config(menu=self.menubar)

        self.path = ''

        self.fig = plt.figure(1)

        # plt.ion()
        # t = np.arange(0.0, 3.0, 0.01)
        # s = np.cos(np.pi * t)
        # plt.plot(t, s)

        canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.plot_widget = canvas.get_tk_widget()
        self.plot_widget.pack(side=BOTTOM)
        # layout

    def init_filemenu(self):
        self.filemenu.add_command(label="Open", command=self.open_dialog)
        self.filemenu.add_command(
            label="Append", command=self.open_dialog_append)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.master.quit)
        # self.filemenu.entryconfigure("Save", state=DISABLED)

    def open_dialog(self):
        self.path = filedialog.askopenfilename()
        data = read_file(self.path)

        plt.clf()
        x_axis = range(len(data))
        plt.plot(x_axis, data)
        self.fig.canvas.draw()

    def open_dialog_append(self):
        self.path = filedialog.askopenfilename()
        data = read_file(self.path)
        x_axis = range(len(data))
        plt.plot(x_axis, data)
        self.fig.canvas.draw()


root = Tk()

gui = GUI(root)

root.mainloop()
