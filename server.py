#!/usr/bin/env python
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

on_heroku = False
if 'MONGOLAB_URI' in os.environ:
  on_heroku = True

if on_heroku:
    client = MongoClient(os.environ['MONGOLAB_URI'])
else:
    client = MongoClient('mongodb://localhost:27017/')

db = client.instachart
collection = db.data

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', header='Instachart', title='Instachart')

if __name__ == '__main__':
    app.run(debug=True)