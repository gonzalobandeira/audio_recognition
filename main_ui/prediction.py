import pickle
import json
import numpy as np
import pandas as pd
from scipy.fftpack import fft
from sklearn.preprocessing import LabelEncoder

from model_design.nn_model import nn_to_labels

# Load automatically model saved in production PATH
with open("../models/model_production.json", "r") as file:
    config = json.loads(file.read())
filename = config["filename"]
prod_model = pickle.load(open(filename, 'rb'))
print("Model {} loaded".format(filename))

# Load label encoder to return categorical values
with open("../config/target_labels.pkl", "rb") as file:
    labeler = pickle.load(file)
print("Labeler loaded")

# Number of features
with open('../config/config.json', 'r') as file:
    config = json.loads(file.read())
feat = config["features"][1]


def model(np_array):
    data_ftt = np.abs(fft(np_array))
    data_ftt = data_ftt[:len(data_ftt) // 2 + 1]

    z = [[]] * data_ftt.shape[0]
    for i, ele in enumerate(data_ftt):
        z[i] = [num for num in ele]

    features = np.array(z).reshape(1, -1)[:, :feat]

    pred = prod_model.predict(features)

    if filename.split("/")[-1] == "model_Neural_Network.sav":
         #print(pred)
        pred = nn_to_labels(pred)

    # print("Prediction: ", pred)

    print(labeler.inverse_transform(pred))
    return labeler.inverse_transform(pred)[0]


