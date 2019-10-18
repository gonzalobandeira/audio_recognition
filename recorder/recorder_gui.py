import os
import webbrowser
from tkinter import *
from tkinter.ttk import *

from recorder.recorder_recording import record


def main():
    def clicked_start():
        status_va.set("Recording...")
        window.update_idletasks()

        settings = {
            "recording_seconds": int(time.get()),
            "chunk": int(chunk.get()),
            "width": int(width.get()),
            "channels": int(channels.get()),
            "rate": int(rate.get()),
        }
        target = combo_target.get()

        path_v_update = record(settings, target)

        status_va.set("Recording finished")
        path_v.set(path_v_update)

    def open_folder():
        cd = os.getcwd()
        path_b = "/".join(cd.split("\\")[:-1]) + "/recordings"
        webbrowser.open(path_b)

    window = Tk()
    window.title("Dataset Recording App")
    window.iconbitmap("./ico/micro.ico")
    window.geometry('450x200')

    btn = Button(window, text="Start Recording", command=clicked_start)
    btn.grid(column=0, row=0)

    lbl = Label(window, text="Target: ")
    lbl.grid(column=3, row=0)

    combo_target = Combobox(window)
    combo_target['values'] = ("microwave", "juice_maker", "dishwasher", "nothing", "water_tap")
    combo_target.current(2)  # set the selected item
    combo_target.grid(column=3, row=0)

    status_va = StringVar()
    status_va.set("")
    status = Label(window, textvariable=status_va)
    status.grid(column=0, row=1)

    path_v = StringVar()
    path_v.set("")
    path = Label(window, textvariable=path_v)
    path.grid(column=2, columnspan=3, row=1)

    btn = Button(window, text="open folder", command=open_folder)
    btn.grid(column=3, row=2)

    lbl = Label(window)
    lbl.grid(column=0, row=2)

    box_size = 8

    lbl = Label(window, text="Time (s): ")
    lbl.grid(column=0, row=3)
    time = Entry(window, width=box_size)
    time.grid(column=1, row=3)
    time.insert(END, 20)

    lbl = Label(window, text="Chunk: ")
    lbl.grid(column=0, row=4)
    chunk = Entry(window, width=box_size)
    chunk.grid(column=1, row=4)
    chunk.insert(END, 1024)

    lbl = Label(window, text="Width: ")
    lbl.grid(column=0, row=5)
    width = Entry(window, width=box_size)
    width.grid(column=1, row=5)
    width.insert(END, 2)

    lbl = Label(window, text="Channels: ")
    lbl.grid(column=0, row=6)
    channels = Entry(window, width=box_size)
    channels.grid(column=1, row=6)
    channels.insert(END, 1)

    lbl = Label(window, text="Rate (Hz): ")
    lbl.grid(column=0, row=7)
    rate = Entry(window, width=box_size)
    rate.grid(column=1, row=7)
    rate.insert(END, 44100)

    window.mainloop()


if __name__ == "__main__":
    main()
