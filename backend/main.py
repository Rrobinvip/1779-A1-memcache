from flask import render_template, url_for, request,jsonify
from backend import app, memcache,usage,itemNum,itemSize,requestNum,missRate,hitRate
from flask import json
import threading


#Data Model
from backend.data import Data

#initialize the database connection
sql_connection = Data()

#stats Model
from backend.stats import Stats
stats_update = Stats()



@app.route('/')
def main():
    return "Here is backend"

@app.route('/test')
def test():
    sql_connection.insert_stat_data(1,2.0,3,0.5,0.5)
    data = sql_connection.get_stat_data()
    return data

@app.route('/statistics')
def stats():
    print("This is running")
    print("Call made")
    thread = threading.Thread(target = stats_update.stats_update, args = (itemNum,itemSize,requestNum,missRate,hitRate))
    thread.start()
    print("Starts")
    return jsonify({
        "success":"true",
        "statusCode":200,
        "message":"this is messgae"
            })
    
    
@app.route('/get', methods=['POST'])
def get():
    key = request.form.get('key')

    if key in memcache:
        value = memcache[key]
        response = app.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = app.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )

    return response


@app.route('/put', methods=['POST'])
def put():
    key = request.form.get('key')
    value = request.form.get('value')
    memcache[key] = value

    response = app.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response
