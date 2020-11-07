# qSort programm 30.10.2020  -  Jeremias Boucsein
#
# Initialisiert die Json Datei, in der die Lern-Datensätze für das KNN gespeichert werden
#
# How to use:
#           Funktion initialize_json_file:
#                 Diese Funktion wird genau EIN mal am Anfang ausgeführt
#                 Als PARAMETER wird eine Liste mit Strings übergeben.
#                 Diese Strings sind die Synonyme (Name oder ID) der Items.
#                 Für jedes Item muss genau EIN Synonym übergeben werden
#                 Die Funktion hat keine Rückgabe
#
import json


def initialize_json_file(objects):
    data = {}
    for name in objects:
        data[name] = {
                'positive': [],
                'negative': []
            }

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)

        
if __name__ == '__main__':
    initialize_json_file(["tomate", "apfel", "birne", "mango"])        
