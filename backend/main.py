from os import stat
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

# Memcache object
from backend.memcache import Memcache
memcache = Memcache()

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
    # status = memcache.getStatus()
    # thread = threading.Thread(target = stats_update.stats_update, args = (status[0],
    #                                                                       status[1],
    #                                                                       status[2],
    #                                                                       status[3],
    #                                                                       status[4]))
    # Threading shares variables. Passing memcache allows it to lively obtain data from it. 
    thread = threading.Thread(target = stats_update.stats_update_t2, args = (memcache, ))
    thread.start()
    print(" * Starts")
    return jsonify({"Messsge":"True, threading starts"}), 200
    
    
@app.route('/get', methods=['GET', 'POST'])
def get():
    # Get key through different approaches.
    key = None
    if request.method == 'GET' and 'key' in request.args:
        key  = escape(request.args.get("key"))
    elif request.method == 'POST':
        key = request.form.get('key')

    value, upload_time = memcache.get(key)
    
    if value != None and upload_time != None:
        print(" - Backend.main.get : Key found in backend! ")
        response = {"key":key, "value":value, "upload_time":upload_time}

        # NOTICE: create a dict and return it with `jsonify`. Another argument after it is the status code. 
        return jsonify(response), 200

    else:
        response = {"Message":"Miss"}
        return jsonify(response), 400



@app.route('/put', methods=['POST'])
def put():
    key = request.form.get('key')
    value = request.form.get('value')
    upload_time = request.form.get('upload_time')

    print(" - Backend: key, upload_time: ", key, upload_time)
    
    result = memcache.put(key, value, upload_time)
    print(" - Backend.main.put v:result: ", result)

    if result:
        returnCode = 200
        returnMessage = {"Message":"Put success"}
    else:
        returnCode = 400
        returnMessage = {"Message":"Put failed"}

    return jsonify(returnMessage), returnCode

@app.route('/clear')
def clear():
    memcache.resetMemcache()
    return jsonify({"Message":"Clear down"}), 200

@app.route('/config', methods=['GET'])
def config():
    size = 100.0
    replacementPolicy = 1
    if "size" in request.args and "replacement_policy" in request.args:
        size = escape(request.args.get("size"))
        replacementPolicy = escape(request.args.get("replacement_policy"))

    sql_connection.insert_config_data(size, replacementPolicy)
    return jsonify({"Message":"Success update config"}), 200