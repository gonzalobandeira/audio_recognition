# https://towardsdatascience.com/music-genre-classification-with-python-c714d032f0d8
import json
import numpy as np
from keras import layers
from keras import models
# import BatchNormalization
from keras.layers.normalization import BatchNormalization
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


def main_model(X, y):

    with open('../config/config.json', 'r') as file:
        config = json.loads(file.read())
    number_classes = int(config["labels"])


    X_train, X_test, y_train, y_test = train_test_split(X, y)

    validation_samples = 10
    x_val = X_train[:validation_samples]
    partial_x_train = X_train[validation_samples:]
    y_val = y_train[:validation_samples]
    partial_y_train = y_train[validation_samples:]

    model = models.Sequential()
    model.add(layers.Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(BatchNormalization())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(number_classes, activation='softmax'))
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(partial_x_train,
              partial_y_train,
              epochs=35,
              batch_size=512,
              validation_data=(x_val, y_val))

    results = model.evaluate(X_test, y_test)
    print("")
    print(results)
    print("\n")

    predictions = model.predict(X_test)

    predictions = nn_to_labels(predictions)
    confusion = confusion_matrix(y_test, predictions)

    return model, confusion


def nn_to_labels(to_change):
    index = []
    res = []
    # Maximum prob means the prediction
    for row in to_change:
        maximo = max(row)
        aux = []
        for ele in row:
            if ele >= maximo:
                ele = 1
            else:
                ele = 0
            aux.append(ele)
        res.append(aux)

    # Return only label, which is the index
    for prediction in res:
        index.append(list(prediction).index(1))

    return index


if __name__ == "__main__":
    test = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    print(nn_to_labels(test))
