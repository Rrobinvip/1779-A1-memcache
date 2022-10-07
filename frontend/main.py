# from crypt import methods
# from fileinput import filename
# from stat import filemode
# from telnetlib import SE
# from traceback import clear_frames

from glob import escape
from flask import render_template, url_for, request, redirect
from flask import json, flash, jsonify
from frontend import app
import requests

# Picture upload form
from frontend.form import UploadForm, pictures

# Data model
from frontend.data import Data
sql_connection = Data()

# Search form
from frontend.form import SearchForm


# Config form 
from frontend.form import ConfigForm
from frontend.form import ClearForm

sql_connection = Data()

#this function calls the backend statistics before the first request
@app.before_first_request
def start():
    r = requests.get("http://127.0.0.1:5000/backend/statistics",timeout = 5)
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
        flash("Upload success")
        print(filename, key)
        sql_connection.add_entry(key, filename)
        return redirect(url_for("upload_picture"))
    
    return render_template("upload.html", form=picture_form)

@app.route("/search", methods=["GET", "POST"])
def search_key():
    search_form = SearchForm()
    filename = None
    upload_time = None
    key = None

    # TODO 
    if request.method == "GET" and "key" in request.args:
        key = escape(request.args.get("key"))
        data = sql_connection.search_key(key)

        if len(data) == 0:
            print("No data")
            flash("No image with this key.")
        else:
            filename = data[0][2]
            upload_time = data[0][3]
            print("Filename: {} upload_time: {}".format(filename, upload_time))


    elif request.method == "POST" and search_form.validate_on_submit():
        key = search_form.key.data
        data = sql_connection.search_key(key)

        if len(data) == 0:
            print("No data")
            flash("No image with this key.")
        else:
            filename = data[0][2]
            upload_time = data[0][3]
            print("Filename: {} upload_time: {}".format(filename, upload_time))
        
    return render_template("search.html", 
                           form = search_form, 
                           tag1_selected=True, 
                           filename=filename, 
                           upload_time=upload_time,
                           key=key)

@app.route("/allpairs")
def all_pairs():
    data = sql_connection.inspect_all_entries()
    
    return render_template("all_pairs.html", items=data, tag2_selected=True)


@app.route("/config", methods=["GET", "POST"])
def memcache_config():
    config_form = ConfigForm()
    clear_form = ClearForm()

    if request.method == "GET" and "size" in request.args and "policy" in request.args:
        # TODO
        # make API call to backend to config memcache
        flash("Update success")
        print("swws")

    if request.method == "POST" and config_form.validate_on_submit():
        size = config_form.size.data
        choice = config_form.replacement_policy.data

        # TODO 
        # make API call to backend to config memcache
        flash("Update success")
        print("++++++++ size and choice: ",size, choice)

    if request.method == "POST" and clear_form.validate_on_submit():
        # TODO make API call to backend to clear memcache
        flash("Memcache cleared.")
        
    return render_template("config.html", form1=config_form, form2=clear_form, tag3_selected=True)

@app.route("/status")
def memcache_status():
    # TODO 
    # make API call to backend to accquire data of memcache status
    test_list = [[0,1,2,3,4]]

    return render_template("status.html", items=test_list, tag4_selected=True)