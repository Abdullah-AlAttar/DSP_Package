import tkinter as tk
from tkinter import ttk

import matplotlib

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import math
from fileprocessing import read_file, read_ds_file, save_ds_file, save_ds_frequency
from data_handler import Data
matplotlib.use("TkAgg")
style.use('bmh')
# style.use('seaborn')
np.set_printoptions(suppress=True)


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
        self.nextBtn = tk.Button(
            self.master, text='Next', command=self.draw_next)
        self.prevBtn = tk.Button(
            self.master, text='Prev', command=self.draw_prev)
        self.prevBtn.pack()
        self.nextBtn.pack()
        self.plot_widget.pack(side=tk.BOTTOM)
        self.counter = 0

    def draw_next(self):
        self.counter += 1
        if self.counter >= len(self.data.signals[0]):
            self.counter -= 1
        plt.clf()
        plt.gca().set_color_cycle(None)
        for signal in self.data.signals:
            # x_axis = range(len(signal))
            # plt.xticks(list(signal.keys()))
            plt.xlim((min(list(signal.keys())) - 1,
                      max(list(signal.keys())) + 1))
            plt.ylim((min(list(signal.values())) - 1,
                      max(list(signal.values())) + 1))
            plt.scatter(list(signal.keys())[:self.counter],
                        list(signal.values())[:self.counter])
        self.fig.canvas.draw()

    def draw_prev(self):
        self.counter -= 1
        if self.counter <= 0:
            self.counter += 1
        plt.clf()
        plt.gca().set_color_cycle(None)
        for signal in self.data.signals:
            # x_axis = range(len(signal))
            plt.xlim((min(list(signal.keys())) - 1,
                      max(list(signal.keys())) + 1))
            plt.ylim((min(list(signal.values())) - 1,
                      max(list(signal.values())) + 1))
            plt.scatter(list(signal.keys())[:self.counter],
                        list(signal.values())[:self.counter])
        self.fig.canvas.draw()

    def init_menubar(self):
        self.file_menu.add_command(
            label="Open Time signal", command=self.open_time_dialog)
        self.file_menu.add_command(
            label="Open Frequency signal", command=self.open_freq_dialog)
        self.file_menu.add_command(
            label="Append", command=self.on_append)
        self.file_menu.add_command(
            label="Save", command=self.on_save)

        self.file_menu.add_command(
            label="Generate Signal", command=self.on_generate)

        self.operations_menu.add_command(
            label="Add", command=self.on_add)
        self.operations_menu.add_command(
            label="Subtract", command=self.on_subtract)
        self.operations_menu.add_command(
            label="Scale", command=self.on_scale)
        self.operations_menu.add_command(
            label="Quantize", command=self.on_quantize)
        self.operations_menu.add_command(
            label="DFT", command=self.on_dft)
        self.operations_menu.add_command(
            label="IDFT", command=self.on_idft)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.menubar.add_cascade(label="Operations", menu=self.operations_menu)

        # self.filemenu.entryconfigure("Save", state=DISABLED)
    def open_freq_dialog(self):
        self.data.signals = []
        self.path = tk.filedialog.askopenfilename()
        freq, amp, phase = read_ds_file(self.path)
        self.data.frequency = (freq, amp, phase)
        self.draw_multi_axes(freq, amp, phase)

    def open_time_dialog(self):
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
        encoding, sample_error = self.data.quantize(levels=self.scalar)
        self.draw_on_canvas(clear=True)
        self.popup_after_quantize(encoding, sample_error)

    def draw_on_canvas(self, clear=False):
        self.counter = len(self.data.signals[0])
        if clear:
            plt.clf()
        plt.gca().set_color_cycle(None)
        for signal in self.data.signals:
            # x_axis = range(len(signal))
            plt.scatter(signal.keys(), signal.values())
        self.fig.canvas.draw()

    def draw_multi_axes(self, freq, amp, phase):
        plt.clf()
        plt.subplot(221), plt.title('Amplitudes')
        plt.scatter(freq, amp)
        plt.subplot(222), plt.title('Phase')
        plt.scatter(freq, phase)
        self.fig.canvas.draw()

    def on_save(self):
        self.path = tk.filedialog.asksaveasfilename()
        save_ds_file(self.path, self.data.signals[0])

    def on_dft(self):
        s = list(self.data.signals[0].values())
        res, amp, phase = self.data.dft(s)

        self.popupmsg('Enter Sampling Frequency ')
        self.scalar = (2 * np.pi) / (len(amp) * (1 / self.scalar))
        freq = [self.scalar * (i + 1) for i in range(len(amp))]

        self.draw_multi_axes(freq, amp, phase)
        x_axis = list(self.data.signals[0].keys())
        save_ds_frequency('./data/outputFreq.ds', x_axis, amp, phase)
        self.data.frequency = (x_axis, amp, phase)
        self.data.signals = []
        print(res)
        print(self.data.fft(s))
        # print(freq)
        # print(amp)
        # print(phase)

    def on_idft(self):

        x = self.data.frequency[1] * np.cos(self.data.frequency[2])
        y = self.data.frequency[1] * np.sin(self.data.frequency[2])
        # x = np.round(x, 4)
        # y = np.round(y, 4)
        res = x + y * 1j
        print('ifft')
        res = self.data.dft(res, inverse=True)
        print(res)
        print(self.data.fft(res, inverse=True))
        print('ifft')
        # res = np.flip(res, 0)
        self.data.signals.append(
            dict(zip(range(len(res)), res.real.tolist())))
        print(self.data.signals[0])
        self.draw_on_canvas(clear=True)
        # res = self.data.dft(self.data.signals[0].values())
        # print(res)

    def on_generate(self):
        self.popupmsg('Sin/Cos,n_samples,Amplitude,theta,F,Fs')
        s_type, n, A, theta, F, Fs = self.popup_return
        n, A, theta, F, Fs = int(n), int(A), int(theta), int(F), int(Fs)
        self.data.generate_signal(s_type, n, A, theta, F, Fs)
        self.draw_on_canvas()

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
            elif self.popup_return.startswith(('sin', 'cos')):
                self.popup_return = self.popup_return.split(',')
            else:
                self.scalar = float(self.popup_return)
            popup.destroy()
            self.master.quit()

        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", padx=12)
        b = ttk.Button(popup, text="Submit", command=on_press)
        input.pack()
        b.pack(side='bottom')
        popup.mainloop()

    def popup_after_quantize(self, encoding, sample_error):

        popup = tk.Tk()
        popup.wm_title("")

        def disable_event():
            popup.destroy()
            self.master.quit()
        popup.protocol("WM_DELETE_WINDOW", disable_event)

        encoding_list = tk.Listbox(popup)
        encoding_list.insert(0, "Encoding")
        sample_error_list = tk.Listbox(popup)
        sample_error_list.insert(0, "Error")
        for i in range(len(encoding)):
            encoding_list.insert(i + 1, encoding[i])
        for i in range(len(sample_error)):
            sample_error_list.insert(i + 1, sample_error[i])
        encoding_list.pack(side='left')
        sample_error_list.pack(side='right')
        popup.mainloop()


root = tk.Tk()
gui = GUI(root)

root.mainloop()
