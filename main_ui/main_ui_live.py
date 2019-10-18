import multiprocessing
import tkinter as Tk

from queue import Empty
from tkinter import StringVar
from tkinter.ttk import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import specgram

from main_ui.recording import live

from recorder import recorder_gui
from model_design import main_models

plt.style.context("classic")


class GuiApp(object):

    def __init__(self):
        self.root = Tk.Tk()
        self.root.title("Appliances Identifier")
        self.root.iconbitmap("ico/micro.ico")
        self.root.geometry('400x200')

        # Start-stop buttons
        self.btn_start = Tk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.btn_start.grid(column=1, row=1, pady=1, padx=5)
        self.btn_stop = Tk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.btn_stop.grid(column=2, row=1, pady=1, padx=5)

        # Add new sounds and train models
        self.btn_start = Tk.Button(self.root, text="Add sounds", command=recorder_gui.main)
        self.btn_start.grid(column=7, row=0, padx=100, pady = 5)
        self.btn_stop = Tk.Button(self.root, text="Train model", command=main_models.main_call, bg="orange red" )
        self.btn_stop.grid(column=7, row=1, pady=5)

        self.status_v = StringVar()
        self.status_v.set("")
        self.status = Label(self.root, textvariable=self.status_v, font=("Arial", 10))
        self.status.grid(column=1, row=2, columnspan=1, )
        self.results_v = StringVar()
        self.results_v.set("")
        self.text_wid = Tk.Label(self.root, textvariable=self.results_v, font=("Arial Bold", 14))
        self.text_wid.grid(column=1, row=3, columnspan=2)
        self.root.after(100, self.plot_graph, frames_q)
        self.root.after(100, self.CheckQueuePoll, info)

        self.fig, self.ax1, = plt.subplots(nrows=1, figsize = (6.5,5))
        self.ax1.set_ylim(top=20000)
        self.ax1.set_ylabel("Frequency (Hz)")
        self.ax1.set_xlabel("Time (s)")

        #self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        #self.graph_widget = self.canvas.get_tk_widget()
        #self.graph_widget.grid(column=1, row=5, columnspan=10, sticky='nsew', padx = 20)

    def plot_graph(self, queue):
        try:

            text = queue.get(0)
            text = np.array(text[0])

            NFFT = 1024  # the length of the windowing segments
            Fs = 44100  # int(1.0 / dt)  # the sampling frequency
            Pxx, freqs, bins, im = self.ax1.specgram(x=text, NFFT=NFFT, Fs=Fs, noverlap=900)

            #self.canvas.draw()
            plt.close("all")

        except Empty:
            pass
            #print("no new data")
        finally:
            pass
            #self.root.after(200, self.plot_graph, queue)

    def CheckQueuePoll(self, c_queue):
        try:
            text = c_queue.get(0)
            # self.text_wid.set('end', text)
            self.results_v.set(text)
            self.root.update_idletasks()
        except Empty:
            pass
        finally:
            self.root.after(100, self.CheckQueuePoll, c_queue)

    def start_recording(self):
        global q
        self.status_v.set("Recording...")
        q.put("start")

    def stop_recording(self):
        global q
        self.status_v.set("Stopped recording")
        q.put("stop")


if __name__ == '__main__':
    q = multiprocessing.Queue()
    info = multiprocessing.Queue()
    frames_q = multiprocessing.Queue()

    q.cancel_join_thread()  # or else thread that puts data will not term
    gui = GuiApp()  # q)
    # t1 = multiprocessing.Process(target=print_b, args=(q,info))
    t1 = multiprocessing.Process(target=live, args=(q, info, frames_q))
    t1.start()
    gui.root.mainloop()
    t1.join()
    print("closed")
