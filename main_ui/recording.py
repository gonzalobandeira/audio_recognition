import json
from queue import Empty
import numpy as np
import pyaudio

import main_ui.prediction as predict

with open('../config/config.json', 'r') as file:
    config = json.loads(file.read())

RATE = config["rate"]
WIDTH = config["width"]
CHANNELS = config["channels"]

############################################################
# Quantity of data to be analyzed every iteration in samples
with open('../config/config.json', 'r') as file:
    config = json.loads(file.read())
CHUNK = config["chunk"]


############################################################


def live(q, info, frames_q):
    while True:
        try:
            command = q.get(0)
            if command == "start":
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(WIDTH),
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                output=True,
                                frames_per_buffer=CHUNK)
                running = 1  # Initialising while condition
                frames_spec = []
                while running:
                    data_b = stream.read(CHUNK)  # read audio stream
                    data = [np.frombuffer(data_b, dtype=np.int16)]
                    txt = predict.model(data)

                    frames_spec += list(data[0])
                    frames_spec = frames_spec[-44100*2:]

                    if len(frames_spec) == 44100*2:
                        frames_q.put([frames_spec])

                    info.put(txt)
                    try:
                        command = q.get(0)
                        if command == "stop":
                            running = 0
                    except Empty:
                        pass
                p.terminate()
                info.put("")
                print("Process Finished")
        except Empty:
            pass
