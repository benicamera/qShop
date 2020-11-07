# qSort programm 30.10.2020  -  Jeremias Boucsein
#
# Programm um die Datensätze aus einem Json File für das KNN vorzubereiten
#
import json
import numpy as np
import data_write


def data_read_to_predict(object):
    with open('data.json') as json_file:
        data = json.load(json_file)

        diff = []

        dates = data[object]['positive'][-4:]           # nutzen der letzten 4 Daten zur Vorhersage
        current_time = data_write.get_time()
        for i in dates:                                 # Berechnen der Zeitdiferenz zu heute
            diff.append((i - current_time) / 10)

        diff.insert(0, 1)               # Einfügen des Bias an den Anfang

        if diff[-1] > -4.0:
            data_predict = np.array(diff)       # schreiben der Daten in ein Numpy Array
            return data_predict
        else:                           # Wenn der Letzte kauf mehr als 40 Tage her ist, braucht nicht mir diesem Item
            # trainiert werden. Somit wird dann eine leere Liste zurückgegeben
            return []


def data_read_negative(object):
    training_data = []

    with open('data.json') as json_file:
        data = json.load(json_file)
        training_data_list = data[object]['negative']
        for i in training_data_list:
            training_data.append((np.array(i[0]), i[1]))

    return training_data


def data_read_positive(object):

    training_data_prep = []
    temp_data = []
    training_data = []
    y_diff = []

    with open('data.json') as json_file:  # öffnen des Daten files
        data = json.load(json_file)
        training_data_list = np.array(data[object]['positive'])   # Speichern der Daten in einer Liste

    for i in range(len(training_data_list)):
        # Errechnen der zeitlichen Differenz zum letzten Kauf und Speichern dieser in Liste
        training_data_prep.append((training_data_list[i] - training_data_list[len(training_data_list)-1]) / 10)

    if len(training_data_prep) >= 5:                    # Speichern von vierer-Datensätzen zum lerenen
        for i in range(len(training_data_prep)):
            if i <= len(training_data_prep) - 5:
                temp_data.append(training_data_prep[i:(i+4)])
                y_diff.append(training_data_prep[i+4])

    for i, d in enumerate(temp_data):                   # Ergänzen um gewünschten Output
        # Errechnet den Abstand zum nächsten Kauf, und speichert diesen dann als Werte fürs Training
        for idx in range(len(d)):
            d[idx] = d[idx] - y_diff[i]
        d.insert(0, 1)                                  # Bias an den Anfang einfügen
        a = np.array(d)
        training_data.append((a, 1))                    # (Erzueugt nur postivi-Beispiele)

    return training_data


if __name__ == '__main__':
    p = data_read_positive('tomate')
    print(p)

    o = data_read_negative('tomate')
    print(o)
