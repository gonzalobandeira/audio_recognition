import json
import pickle

import pandas as pd

from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier

# from xgboost import XGBClassifier

from sklearn.multiclass import OneVsOneClassifier
import model_design.nn_model as nn

with open("../config/target_labels.pkl" , "rb") as file:
    labeler = pickle.load(file)

def test_models(data, target):
    #TO TEST
    nn_models = True
    ml_models = True

    # SINGLE_CLASS models
    models = {
        # "Logistic Regression": LogisticRegression(solver="lbfgs"),
        # "SVM_C": SVC(gamma="auto"),
        # "Random_Forest_n_10": RandomForestClassifier(n_estimators=10),  # SC and MC
        # "DecisionTreeClass": DecisionTreeClassifier(),  # SC and MC
        # "KNeighbors": KNeighborsClassifier(),  # SC and MC
        # "GradientBooster": GradientBoostingClassifier(),
    }
    # MULTI_CLASS models
    models_mc = {
        #"Random_Forest_n_10": RandomForestClassifier(n_estimators=10),  # SC and MC
        #"DecisionTreeClass": DecisionTreeClassifier(),  # SC and MC
        "KNeighbors": KNeighborsClassifier(n_neighbors=6),  # SC and MC
        # "GradientBooster": GradientBoostingClassifier(),
    }

    X = data
    print("X shape: {}".format(X.shape))
    y = target.squeeze()


    # Save number of features
    with open('../config/config.json', 'r') as file:
        config = json.loads(file.read())
    config["features"] = X.shape
    with open("../config/config.json", "w+") as file:
        json.dump(config, file)

    # Neural Network
    if nn_models:
        print("Training Neural Network: ")
        nn_model, nn_conf = nn.main_model(X, y)
        print(nn_conf)
        filename = '../models/testing/model_NeuralNetwork.sav'
        pickle.dump(nn_model, open(filename, 'wb'))

        print("Target values: {} ".format(labeler.inverse_transform(y.unique())))

    if ml_models:
        if len(y.value_counts().index) > 2:
            # Multi-Class modelling
            scores = {}
            for label, model in models_mc.items():
                print("Computing multi-class CV: {}".format(label))
                model = OneVsOneClassifier(model)
                scores[label] = cross_val_score(model, X, y, cv=5).mean()

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)

            predictions = []
            for label, model in models_mc.items():
                model = OneVsOneClassifier(model)
                print("Computing multi-class train/test split: {}".format(label))
                pred = model.fit(X_train, y_train).predict(X_test)
                predictions.append({
                    "model": label,
                    "Confusion_Matrix": confusion_matrix(y_test, pred)
                })

            results(scores, predictions)


            for label, model in models_mc.items():
                print("Saving {}".format(label))
                filename = '../models/testing/model_multi_{}.sav'.format(label)
                pickle.dump(model, open(filename, 'wb'))


        else:
            # Single-Class modelling
            scores = {}
            for label, model in models.items():
                print("Computing single-class: {}".format(label))
                scores[label] = cross_val_score(model, X, y, cv=5).mean()

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
            predictions = []
            for label, model in models.items():
                pred = model.fit(X_train, y_train).predict(X_test)
                predictions.append({
                    "model": label,
                    "f1_score": f1_score(y_test, pred),
                    "Confusion_Matrix": confusion_matrix(y_test, pred)
                })

            results(scores, predictions)

            for label, model in models.items():
                filename = '../models/testing/model_single_{}.sav'.format(label)
                pickle.dump(model, open(filename, 'wb'))


def prod_model(X, y, model):
    if len(y.value_counts().index) > 2:
        model = OneVsOneClassifier(model)
    model.fit(X, y)
    return model


def save_prod_model(model, name):
    filename = '../models/model_{}.sav'.format(name)
    with open(filename, 'wb') as file:
        pickle.dump(model, file)

    json_file = {
        "filename": filename,
    }
    with open('../models/model_production.json', 'w+') as file:
        json.dump(json_file, file)


def results(scores, predictions):
    predictions_df = pd.DataFrame(predictions)
    scores_df = pd.DataFrame.from_dict(scores, orient="index").reset_index()
    scores_df.columns = ["model", "Score CV"]
    result = predictions_df.merge(scores_df, how="left", on="model")
    print("Results: \n")
    print(result)
