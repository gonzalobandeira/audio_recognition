import pandas as pd
from model_design.modelling import test_models, prod_model, save_prod_model
from model_design.dataset_making import make_data
from model_design.transform import transform
import model_design.nn_model as nn

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def main_call():
    ########################################################################
    # True if testing different models. False to train the chosen model
    testing = False
    # Only if testing = False. Save NN model as production model. If False save ML model
    nn_flag = True

    if nn_flag:
        # NN
        name = "Neural_Network"
    else:
        # ML
        name = "KNN"
        model = KNeighborsClassifier()
    # True if new audio needs to be transform and included into new features
    new_audio = True
    ########################################################################

    if new_audio:
        # Create Dataset
        make_data()

        # Read dataset
        data = pd.read_csv("../data/dataset.csv")

        # Convert into Freq Domain
        print("Converting into frequency domain: ...")
        X, y = transform(data)
        print("Done.")
        print("Features: {}".format(X.shape))
    else:
        X = pd.read_csv("../data/X_f.csv")
        y = pd.read_csv("../data/y.csv")

    # Explore models

    if testing:
        print("Testing models: ...")
        test_models(X, y)
    else:
        print("Training final model: ...")

        if nn_flag:
            print("           Model: {}".format(name))
            y = y.squeeze()
            nn_model, _ = nn.main_model(X, y)
            save_prod_model(nn_model, name)
        else:
            print("           Model: {}".format(name))
            y = y.squeeze()
            model = prod_model(X, y, model)
            save_prod_model(model, name)


        print("Saved")

if __name__ == "__main__":
    main_call()