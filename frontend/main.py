from crypt import methods
from fileinput import filename
from stat import filemode
from telnetlib import SE
from flask import render_template, url_for, request, redirect
from flask import json, flash
from frontend import app

# Picture upload form
from frontend.form import UploadForm, pictures

# Data model
from frontend.data import Data

# Search form
from frontend.form import SearchForm

sql_connection = Data()

@app.route('/')
def main():
    return redirect(url_for("upload_picture"))


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
    
    return render_template("upload.html", form = picture_form)

@app.route("/allpairs")
def all_pairs():
    data = sql_connection.inspect_all_entries()
    
    return render_template("all_pairs.html", items=data, tag2_selected=True)

@app.route("/search", methods=["GET", "POST"])
def search_key():
    search_form = SearchForm()
    filename = None
    upload_time = None
    key = None

    if request.method == "POST" and search_form.validate_on_submit():
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