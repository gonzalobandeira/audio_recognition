import json

import numpy as np
import pandas as pd
from scipy.fftpack import fft


def transform(data_t):
    # Save X and y
    target_col = data_t.columns[-1]
    X_t = data_t.drop(columns=target_col)
    y = data_t[target_col]

    # Transform X to frequency domain
    data_ftt = X_t.apply(lambda x: np.abs(fft(x)[:len(fft(x)) // 2 + 1]), axis=1)
    z = [[]] * data_ftt.shape[0]
    for i, ele in enumerate(data_ftt):
        z[i] = [num for num in ele]
    X_f = pd.DataFrame(z)

    X_f.to_csv("../data/X_f.csv", header=True, index=False)
    y.to_csv("../data/y.csv", header=True, index=False)

    # Save number of features
    with open('../config/config.json', 'r') as file:
        config = json.loads(file.read())
    config["features"] = X_f.shape
    with open("../config/config.json", "w+") as file:
        json.dump(config, file)

    return X_f, y


if __name__ == "__main__":
    data = pd.read_csv("../data/dataset.csv")
    transform(data)
