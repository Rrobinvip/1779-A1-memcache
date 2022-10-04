from flask import render_template, url_for, request
from backend import app, memcache
from flask import json


@app.route('/')
def main():
    return render_template("main.html")


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
