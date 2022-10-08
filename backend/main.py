from flask import render_template, url_for, request,jsonify
from backend import app, memcache,usage,itemNum,itemSize,requestNum,missRate,hitRate
from flask import json
import threading
from glob import escape


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

#This is front back call example
@app.route('/test')
def test():
    message = "This is message"
    #generate the json response
    response = jsonify({
        "success":"true",
        "status":200,
        "message":message
    })
    #return json response
    return response

@app.route('/statistics')
def stats():
    print(" * This is running")
    print(" * Call made")
    thread = threading.Thread(target = stats_update.stats_update, args = (itemNum,itemSize,requestNum,missRate,hitRate))
    thread.start()
    print(" * Starts")
    return jsonify({
        "success":"true",
        "status":200
            })
    
    
@app.route('/get', methods=['GET', 'POST'])
def get():
    # Get key through different approaches.
    if request.method == 'GET' and 'key' in request.args:
        key = key = escape(request.args.get("key"))
    elif request.method == 'POST':
        key = request.form.get('key')

    if key in memcache:
        value = memcache[key]
        response = {"key":key, "value":value}

        # NOTICE: create a dict and return it with `jsonify`. Another argument after it is the status code. 
        return jsonify(response), 200
        
        # response = app.response_class(
        #     response=json.dumps(value),
        #     status=200,
        #     mimetype='application/json'
        # )
    else:
        response = {"key":key, "value":"None"}
        return jsonify(response), 400



@app.route('/put', methods=['POST'])
def put():
    key = request.form.get('key')
    value = request.form.get('value')
    upload_time = request.form.get('upload_time')
    memcache[key] = value

    response = app.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response
