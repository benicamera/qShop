# API 01.01.2021  -  Benjamin Dangl
#
# Verbindung zwischen Frontend und Backend
#
from flask import Flask, request, jsonify

import initialise_json_file as init_json
import data_write
import knn_learn_and_predict as prdct

app = Flask(__name__)

# Approute = *Lokale IP*/api


@app.route('/api', methods=['GET'])
def hello_world():
    # 'Query':
    # http://127.0.0.1:5000/api?Query=hello world
    # Query = str(request.args['Query'])
    # return Query
    # gibt 'hello world' zurück
    Query = str(request.args['Query'])
    recived = query(Query)
    # Flutter kann nur JSON lesen
    d = {}
    d['Query'] = recived
    return jsonify(d)


# Benutzte HTPP-Codes:
# 200 - "OK"
# 400 - "Bad Request" (Argumentfehler)
# 404 - "Not found" (falscher Befehl)
# 500 - "Server Error" (fehler im Python-script)
def query(_query):
    try:
        Query = _query
        if Query.split(" ")[0] == '0001':
            #TODO: Alle Standard Produkte. Kommt entweder von Flutter oder wird hier irgendwo initialisiert
            init_json.initialize_json_file('Apfel')
            return '200'

        if Query.split(" ")[0] == '0002':
            if len(Query.split(" ")) == 1:
                return '400'

            data_write.data_write_positive(item_name_from_query(Query))
            return '200'

        if Query.split(" ")[0] == '0003':
            data_write.data_write_negative()
            return '200'

        if Query.split(" ")[0] == '0004':
            return prdct.learn_and_predict(pred_list("".join(Query.split(" ")[1:])))

        return '404'
    except:
        return '500'


def pred_list(item_string):
    return item_string.split(",")


def item_name_from_query(_query):
    return "".join(_query.split(" ")[1:])


if __name__ == '__main__':
    app.run()
