import json
import os
import re

import numpy as np
import pyaudio
from pydub import AudioSegment


def record(settings, target):
    config = {
        "chunk": settings["chunk"],
        "width": settings["width"],
        "channels": settings["channels"],
        "rate": settings["rate"],
        "record_seconds": settings["recording_seconds"],
    }

    # Save config data to be used later in scripts
    with open("../config/config.json", "w+") as file:
        json.dump(config, file)

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(config["width"]),
                    channels=config["channels"],
                    rate=config["rate"],
                    input=True,
                    output=True,
                    frames_per_buffer=config["chunk"])

    print("* recording")

    frames = []
    frames_b = []
    for i in range(0, int(config["rate"] / config["chunk"] * config["record_seconds"])):
        data = stream.read(config["chunk"])  # read audio stream
        frames_b.append(data)
        frames.append(np.frombuffer(data, dtype=np.float32))
    p.terminate()

    flat_list = []
    for sublist in frames_b:
        for item in sublist:
            flat_list.append(item)

    sound_recorded = AudioSegment(
        data=bytes(flat_list),
        sample_width=config["width"],
        frame_rate=config["rate"],
        channels=config["channels"]
    )

    sound_recorded = sound_recorded._spawn(frames)

    count = get_number_files(target)
    sound_recorded.export("../recordings/{}/{}_{}.wav".format(target, target, count), format="wav")

    print("* done")
    print("../recordings/{}/{}_{}.wav".format(target, target, count))
    return "../recordings/{}/{}_{}.wav".format(target, target, count)


def get_number_files(target):
    # Check folder exists. If not create it
    for root, dirs, files in os.walk("../recordings"):
        if (target not in dirs) and (root == "../recordings"):
            os.mkdir("../recordings/" + target)

    # Return next number of file
    for root, dirs, files in os.walk("../recordings/{}".format(target), topdown=False):
        return len([re.findall(target, name) for name in files]) + 1


if __name__ == "__main__":
    s = {
        "recording_seconds": 4,
        "chunk": 1024,
        "width": 2,
        "channels": 1,
        "rate": 44100,
    }
    record(s, "dishwasher")
    # get_number_files("dishwasher")
