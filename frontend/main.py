from crypt import methods
from flask import render_template, url_for, request, redirect
from flask import json, flash
from frontend import app
from frontend.form import UploadForm, pictures

# Data model
from frontend.data import Data

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