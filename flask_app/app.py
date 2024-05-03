from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import certifi
import os
app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://yer:HUtySU4t80h55iXJ@cluster0.vz6chxl.mongodb.net/Cluster0?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = str(os.urandom(16))

mongo = PyMongo(app, tlsCAFile=certifi.where())

@app.route('/')
def hello_world():
    return 'Hello'


@app.route('/login', methods = ['GET', 'POST'])
def login():
    return render_template('loginregister.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('loginregister.html')


@app.route('/experience', methods = ['GET'])
def experience():
    return render_template('experience.html')

@app.route('/projects', methods = ['GET'])
def projects():
    return render_template('projects.html')

@app.route('/reviews', methods = ['GET', 'POST'])
def reviews():
    return render_template('/reviews.html')