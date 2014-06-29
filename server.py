#!/usr/bin/env python
from flask import Flask, render_template, request
from pymongo import MongoClient
import os
from bson.objectid import ObjectId
import json

import StringIO
import csv

import sys

app = Flask(__name__)

on_heroku = False
if 'MONGOLAB_URI' in os.environ:
  on_heroku = True

if on_heroku:
    db = MongoClient(os.environ['MONGOLAB_URI'])
    collection = db.data
else:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.instachart
    collection = db.data


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', header='Instachart', title='Instachart')

def throw_parse_error():
    print sys.exc_info()
    print "Unexpected error:", sys.exc_info()[0]
    sys.stdout.flush()
    return render_template('index.html', header='Instachart', title='Instachart', body_message="Data failed to parse. Please try again and follow the format described.")

@app.route('/generate/pie', methods=['POST'])
def generate_pie():
    try:
        chart_id = None
        f = StringIO.StringIO(request.form['data'])
        reader = csv.reader(f, delimiter=',')
        data = []
        for row in reader:
            try:
                data.append({
                    'label': str(row[0]),
                    'value': float(str(row[1]).strip())
                })
            except:
                return throw_parse_error()
        chart_id = str(collection.insert({'data': data}))
        if chart_id is not None:
            return render_template('redirect.html', redirect_location="/chart/" + chart_id)
        else:
            return throw_parse_error()
    except:
        return throw_parse_error()

@app.route('/chart/<id>', methods=['GET'])
def view_chart(id):
    chart_data = collection.find_one(ObjectId(id))['data']
    return render_template('pie_chart.html', chart_data=json.dumps(chart_data), chart_id=id)

if __name__ == '__main__':
    app.jinja_env.globals.update(base_url='http://instachart.herokuapp.com')
    app.run(debug=True)