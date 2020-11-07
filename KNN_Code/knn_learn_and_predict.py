# qSort programm 31.10.2020  -  Jeremias Boucsein
#
# Programm um das KNN einzulerenen und eine Vorhersage von ihm umzuformatieren
#
# How to use:
#           Funktion learn_and_predict:
#                   Diese Funktion wirde jeden Morgen einmal aufgerufen, um die Vorschläge für den Tag zu errechnen.
#                   Als PARAMETER wird ihr eine Liste von Strings übergeben. Die Strings sind die Items bzw.
#                   deren ID.
#                   Als Rückgabe wird eine Liste an Strings zurückgegeben. Die Strings sind auch hier die Items bzw.
#                   deren ID. Die zurückgegebenen Items in der Liste sind die Items, die dem Nutzer der App
#                   vorgeschlagen werden sollen. Dabei ist das erste Item in der Liste das, das am wahrscheinlichsten
#                   gekauft wird.
#
from data_read import data_read_positive, data_read_negative, data_read_to_predict
from bubble_sort_hussein import bubblesort
import KNN
from numpy import random
import numpy as np


def get_training_data(object):
    training_data = []
    pos_examples = data_read_positive(object)
    neg_examples = data_read_negative(object)

    while len(neg_examples) > len(pos_examples):
        del neg_examples[random.randint(0, len(neg_examples))]

    training_data.extend(pos_examples)
    training_data.extend(neg_examples)

    return training_data


def learn_and_predict(list_objects):
    prediction_output = []
    item_list_output = []
    for object in list_objects:

        knn = KNN.MLP(eta=0.03, iterations=30000, n_input_neurons=4, n_hidden_neurons=3)

        p_data = data_read_to_predict(object)       # Daten zur Vorhersage

        if len(p_data) > 0:             # Wenn das Objekt das letzte mal vor länger als 40 Tagen gekauft wurde,
            # ist der Return von data_read_to_predict() eine leere Liste. Dann soll das Netzt, um die Rechenzeit zu
            # minmieren, nicht mit dem Datensatz trainiert werden. Es wird eine Prediction von 0 zurückgegeben.
            t_data = get_training_data(object)      # Daten zum trainieren
            if len(p_data) == 5 and len(t_data) == 10:      # Nur wenn alle Daten richtig formatiert sind

                knn.fit(t_data)                 # trainieren des KNN

                pre = knn.predict(p_data)       # KNN errechnen die Vorhersage

                knn.plot()                      # erstellt einen Plot (zum Debuggen)

                prediction_output.append(pre)
                item_list_output.append(object)
        else:
            prediction_output.append(np.array([0]))     # 0 als Array für die Einheitlichkeit
            item_list_output.append(object)

    bubblesort(prediction_output, item_list_output)

    output = []
    for i, o in enumerate(item_list_output):       # Nur Items mit einer Kaufwahrscheinlichkeit von
        # über 60 % vorschlagen. Und Umsortierne, sodass das wahrscheinlichste am Anfang ist
        if prediction_output[i] > 0.6:
            output.insert(0, o)

    return output


if __name__ == '__main__':
    objekte = ["apfel", "karotte", "birne", "tomate", "mango"]

    p = learn_and_predict(objekte)
    print(p)
