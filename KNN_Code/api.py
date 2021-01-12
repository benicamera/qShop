# API 01.01.2021  -  Benjamin Dangl
#
# Verbindung zwischen Frontend und Backend
#
import json

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
    Query = str(request.args['Query'])
    print("Print", Query)
    #JSON
    recived = query(Query)
    # Flutter kann nur JSON lesen
    d = {'Query': recived}
    return jsonify(d)


# Benutzte HTPP-Codes:
# 200 - "OK"
# 400 - "Bad Request" (Argumentfehler)
# 404 - "Not found" (falscher Befehl)
# 500 - "Server Error" (Fehler im Python-script)
def query(_query):
    try:
        Query = _query
        if Query.split(" ")[0] == '0002':
            if len(Query.split(" ")) == 1:
                return {'Code': '400', 'Query': []}

            newJson = data_write.data_write_positive(item_name_from_query(Query), jsonStringFromQueryWName(Query))
            return {'Code': '200', 'Query': json.loads(newJson)}

        if Query.split(" ")[0] == '0003':
            if len(Query.split(" ")) == 1:
                return {'Code': '400', 'Query': []}

            newJson = data_write.data_write_negative(item_name_from_query(Query), jsonStringFromQueryWName(Query))
            return {'Code': '200', 'Query': json.loads(newJson)}

        if Query.split(" ")[0] == '0004':
            if len(Query.split(" ")) == 0:
                return {'Code': '400', 'Query': []}
            return {'Code': '200', 'Query': prdct.learn_and_predict(Query)}

        return {'Code': '404', 'Query': []}

    except:
        return '500'


def pred_list(item_string):
    return item_string.split(",")


def jsonStringFromQueryWName(query):
    return "".join(query.split(" ")[2:])


def item_name_from_query(_query):
    return "".join(_query.split(" ")[1])


if __name__ == '__main__':
    app.run()

