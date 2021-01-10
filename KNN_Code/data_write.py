# qSort programm 30.10.2020  -  Jeremias Boucsein
#
# Speichert die Daten für das KNN in einer Json Datei
#
# How to use:
#           Funktion data_write_positive:
#                      Diese Funktion wird jedesmal wenn ein Objekt gekauft wurde aufgerufen.
#                      Sie darf NICHT VOR der initialize_json_file Funktion aufgerufen werden.
#                      Wenn ein Objekt vom Nutzer neu erstellt wurde,
#                      sodass es NICHT in der initialize_json_file Funktion inizialisiert wurde,
#                      kann es DENNOCH an die Funktion übergeben werden.
#                      Die Funktion initialisiert das neue Objekt dann.
#                      Als PARAMETER wird der Funktion ein String übergeben.
#                      Dieser String ist der Name/die ID des Objekts, das gekauft wurde.
#                      Die Funktion hat keine Rückgabe.
#           Funktion data_write_negative:
#                      Diese Funktion soll alle 25 Stunden einmal aufgerufen werden.
#                      Sie hat keine Parameter und keine Rückgabe
#
import time
import json
from numpy import random
from bubble_sort_hussein import get_time


def data_write_positive(object):
    with open('data.json') as json_file:
        data = json.load(json_file)

        if object not in data:      # Wenn das Objket noch nicht vorhanden ist, erstelle es
            data[object] = {
                'positive': [],
                'negative': []
            }

        temp = data[object]['positive']

        y = get_time()  # Aufrufen des Datums relativ zum 1.1.2020

        temp.append(y)  # Daten zu 'positive' hinzufügen

        if len(temp) > 9:  # es braucht nur 9 Daten zu speichern, das reicht zum training
            del temp[0]

    with open('data.json', 'w') as f:      # Den Alten Datensatz durch den neuen überschreiben
        json.dump(data, f, indent=4)


def data_write_negative():
    do_it = False

    with open('data.json') as json_file:
        data = json.load(json_file)

        for obj in data:
            if len(data[obj]['positive']) >= 4:     # Nur wenn des mindestens 4 Werte gibt
                temp_list = data[obj]['positive'][-4:]  # Die letzten vier Daten aus dem Datenzatz nutzen
                current_date = get_time()

                for h in range(len(temp_list)):     # Errechnen der Zeitdifferenz zu heute
                    temp_list[h] = (temp_list[h] - current_date) / 10

                temp_list.insert(0, 1)              # Hinzufügen des Bias an den Anfang

                if temp_list[-1] != 0:   # Wenn das Objekt heute nicht gekauft wurde,
                    # kann das heutige Datum als Negativ-Beispiel verwendet werden
                    do_it = True

                    data[obj]['negative'].append(temp_list)

                    if len(data[obj]['negative']) > 9:      # begrenzt Anzahl an Negativ-Beispielen
                        random_number = random.randint(0, 9)    # Um keinen zu gleichmäßigen Datensatz zu erhalten
                        del data[obj]['negative'][random_number]

    if do_it:                   # nur wenn mindestens eine Änderung vogenommen wurde
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)


if __name__ == '__main__':
    liste = ["apfel", "karotte", "birne", "tomate", "mango", "trauben", "salat", "brot", "toast", "marmelade", "schokolade", "kekse", "nudeln", "reis"]
    # data_write_positive('tomate')
    for i in range(11):
        for o in liste:
            data_write_positive(o)
        r = random.randint(1, 4)  # in sekunden
        time.sleep(r)
        data_write_negative()
        time.sleep(5 - r)
