# from crypt import methods
# from fileinput import filename
# from stat import filemode
# from telnetlib import SE
# from traceback import clear_frames

from cmath import log
from glob import escape
from tkinter.messagebox import NO
from flask import render_template, url_for, request, redirect
from flask import json, flash, jsonify
from frontend import app
import requests
import logging
from datetime import datetime

# Picture upload form
from frontend.form import UploadForm, pictures

# Data model
from frontend.data import Data

# Search form
from frontend.form import SearchForm

# Config form 
from frontend.form import ConfigForm
from frontend.form import ClearForm

# Helper
from frontend.helper import api_call

# Encode and decode img
from frontend.helper import write_img_local, image_encoder, current_datetime

sql_connection = Data()

#this function calls the backend statistics before the first request
@app.before_first_request
def start():
    r = api_call("GET", "statistics")
    print("Response: ", r)
    if r.status_code == 200:
        print("Frontend and backend connection success.")
    pass

@app.route('/')
def main():
    return redirect(url_for("upload_picture"))

#This function is front back call example
@app.route('/test')
def test():
    #call the backend url
    request = requests.get("http://127.0.0.1:5000/backend/test",timeout = 5)
    #parse the json file
    result = request.json()
    #access content in json file
    print(result["success"])
    print(result["status"])
    print(result["message"])
    return "This is front end test"
    
@app.route('/upload', methods=["GET", "POST"])
def upload_picture():
    picture_form = UploadForm()

    if request.method == "POST" and picture_form.validate_on_submit():
        filename = pictures.save(picture_form.pictures.data)
        key = picture_form.key.data

        # Frontend will encode the image into a string, and pass it to backend as a value. 
        value = image_encoder(filename)
        upload_time = current_datetime()
        parms = {"key":key, "value":value, "upload_time":upload_time}
        result = api_call("POST", "put", parms)

        if result.status_code == 200:
            print(" - Frontend: backend stores image into memcache.")
        else:
            print(" - Frontend: memcache failed to store image for unknown reason. Image will still be stored locally. ")

        # After update it with the memcache, frontend will add filename and key into db. 
        flash("Upload success")
        print(filename, key)
        sql_connection.add_entry(key, filename)
        return redirect(url_for("upload_picture"))
    
    return render_template("upload.html", form=picture_form)

@app.route("/search", methods=["GET", "POST"])
def search_key():
    '''
    This function is used to search for the key entered by the user.
    Workflow: The front end will first initiate a search with the back end, if the back end returns an error code 400, 
    the front end will initiate a search to the database. If the backend returns code 200, the frontend will decode the 
    backend image and store it in the local cache. No matter what the result is, if there is an image matching the user's 
    search key, it will be displayed on the web page
    '''
    search_form = SearchForm()
    filename = None
    upload_time = None
    key = None
    cache_flag = False

    print("* Search init...")
 
    # Get key through different approaches. 
    if (request.method == "GET" and "key" in request.args):
        key = escape(request.args.get("key"))
        # Call backend
        print(" - Frontend.main.search_key : Searching in memcache..")
        data = api_call("GET", "get", {"key":key})

        # If the backend misses, look up the database. If the backend hits, decrypt the image and store it
        if data.status_code == 400:
            print("\t Backend doesn't hold this value, try search in DB..")
            data = sql_connection.search_key(key)
            if len(data) == 0:
                print("\t DB doesn't hold this value. Search end.")
                flash("No image with this key.")
            else:
                filename = data[0][2]
                upload_time = data[0][3]
                print("Filename: {} upload_time: {}".format(filename, upload_time))
        elif data.status_code == 200:
            data = data.json()
            value = data["value"]
            upload_time = data["upload_time"]
            filename = "image_local_"+key+current_datetime()+".png"

            write_img_local(filename, value)
            cache_flag = True
            print("Filename: {} upload_time: {}".format(filename, upload_time))
    elif request.method == "POST" and search_form.validate_on_submit():
        key = search_form.key.data

        # Call backend
        print(" - Frontend.main.search_key : Searching in memcache..")
        data = api_call("GET", "get", {"key":key})

        # This part, where requesting data from memcache, is exactly same as above. Becaause I don't have any good 
        # ideas to put them into a function. 

        # If the backend misses, look up the database. If the backend hits, decrypt the image and store it
        if data.status_code == 400:
            print("\t Backend doesn't hold this value, try search in DB..")
            data = sql_connection.search_key(key)
            if len(data) == 0:
                print("\t DB doesn't hold this value. Search end.")
                flash("No image with this key.")
            else:
                filename = data[0][2]
                upload_time = data[0][3]
                print("Filename: {} upload_time: {}".format(filename, upload_time))
        elif data.status_code == 200:
            data = data.json()
            value = data["value"]
            upload_time = data["upload_time"]
            filename = "image_local_"+key+".png"

            write_img_local(filename, value)
            cache_flag = True
            print("Filename: {} upload_time: {}".format(filename, upload_time))


    return render_template("search.html", 
                           form = search_form, 
                           tag1_selected=True, 
                           filename=filename, 
                           upload_time=upload_time,
                           key=key,
                           cache_flag=cache_flag)

@app.route("/allpairs")
def all_pairs():
    data = sql_connection.inspect_all_entries()
    
    return render_template("all_pairs.html", items=data, tag2_selected=True)


@app.route("/config", methods=["GET", "POST"])
def memcache_config():
    config_form = ConfigForm()
    clear_form = ClearForm()

    size = 100.0
    choice = 1

    if request.method == "GET" and "size" in request.args and "policy" in request.args:
        size = escape(request.args.get("size"))
        choice = escape(request.args.get("choice", type=int))
        parms = {"size":size, "replacement_policy":choice}
        result = api_call("GET", "config", parms)

        if result.status_code == 200:
            flash("Update success")
        else: 
            flash("Update failed")
        return redirect(url_for("memcache_config"))


    elif request.method == "POST" and config_form.validate_on_submit():
        size = config_form.size.data
        choice = config_form.replacement_policy.data

        parms = {"size":size, "replacement_policy":choice}
        result = api_call("GET", "config", parms)

        if result.status_code == 200:
            flash("Update success")
        else: 
            flash("Update failed")
        return redirect(url_for("memcache_config"))

    if request.method == "POST" and clear_form.validate_on_submit():
        result = api_call("GET", "clear")

        if result.status_code == 200:
            flash("memcache cleared")
        else: 
            flash("Update failed")
        return redirect(url_for("memcache_config"))
        
    return render_template("config.html", form1=config_form, form2=clear_form, tag3_selected=True)

@app.route("/status")
def memcache_status():
    # TODO 
    # make API call to backend to accquire data of memcache status
    # test_list = [[0,1,2,3,4]]

    r = requests.get("http://127.0.0.1:5001/backend/test",timeout = 5)
    print("Response in test: ", r.json())
    respose = r.json()
    
    test_list = [[1,2,3,4,5,6]]
    # test_list[0] = respose[0][1:]
    
    print("TEST LIST : ", test_list)

    return render_template("status.html", items=test_list, tag4_selected=True)

