import glob
import json
import pickle

import pandas as pd
from pydub import AudioSegment
from sklearn.preprocessing import LabelEncoder

def make_data():
    with open('../config/config.json', 'r') as file:
        config = json.loads(file.read())
    print(config)

    frame_rate = config["rate"]

    ###############################################################################
    # Defines length of each row of the dataset in seconds and saves to config file
    sec_chunk = 0.25  # 0.5
    # Divide recordings in smaller chunks
    chunk = int(frame_rate * sec_chunk)

    ###############################################################################

    # Search for all .wav files
    wav_list = glob.glob('../recordings/**/*.wav')
    df_wav = pd.DataFrame(wav_list, columns=["fname"])
    df_wav["target"] = df_wav["fname"].apply(lambda x: x.split("\\")[1])
    print("Files in dataset: :", df_wav)


    dataset = []
    target = []
    for i in range(df_wav.shape[0]):
        audio = AudioSegment.from_wav(df_wav.iloc[i]["fname"])
        samples = audio.get_array_of_samples()
        for j in range(len(samples) // chunk):
            dataset.append(samples[j * chunk:(j + 1) * chunk])
            target.append(df_wav.iloc[i]["target"])
    dataset = pd.DataFrame(dataset)
    dataset["target"] = target
    dataset.columns = list(range(dataset.shape[1] - 1)) + ["target"]

    if len(dataset.target.value_counts().index) > 2:
        # Multi-class problem -> Label_Encoding
        print("Multi-class Dataset")
        labels = dataset.target.value_counts().shape[0]
        labeler = LabelEncoder().fit(dataset.target)

        # Save labeler object values for later use
        with open("../config/target_labels.pkl", "wb") as file:
            pickle.dump(labeler, file)

        dataset["target"] = labeler.transform(dataset.target)


    else:
        # Single-class encoding
        print("Single-class Dataset")
        #dataset = pd.get_dummies(dataset, columns=["target"])
        #dataset.drop(columns=[dataset.columns[-1]], inplace=True)

        labeler = LabelEncoder().fit(dataset.target)
        # Save labeler object values for later use
        with open("../config/target_labels.pkl", "wb") as file:
            pickle.dump(labeler, file)

        dataset["target"] = labeler.transform(dataset.target)


    # Save dataset to csv
    print("Dataset shape: ", dataset.shape)
    print("Dataset columns: ", dataset.columns)
    dataset.to_csv("../data/dataset.csv", header=True)

    # Save config data
    config["chunk"] = chunk
    config["labels"] = labels
    with open("../config/config.json", "w+") as file:
        json.dump(config, file)


if __name__ == "__main__":
    make_data()
