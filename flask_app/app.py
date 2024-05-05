from flask import Flask, render_template, redirect, request, url_for, session
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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            # User found, log them in and redirect to reviews page
            session['user'] = user['username']
            return redirect(url_for('reviews'))
        else:
            # User not found, display an error message
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if mongo.db.users.find_one({'username': username}) is not None:
            return render_template('register.html', error='Username already exists, try logging in.')
        else:
            mongo.db.users.insert_one({'username': username, 'password': password})
            return redirect(url_for('login'))
    else:
        return render_template('register.html')

# TODO
@app.route('/experience', methods = ['GET'])
def experience():
    return render_template('experience.html')

# TODO
@app.route('/projects', methods = ['GET'])
def projects():
    return render_template('projects.html')

# TODO
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    user = session.get('user')
    if user is not None:
        # User is logged in, pass the username into the template so when they leave a review, it will be associated with their username
        print(user)
        return render_template('/reviews.html', username=session['user'], logged_in=True)
    else:
        # If the user is not logged in, they can still view the reviews page, they just cannot leave a review
        return render_template('/reviews.html', logged_in=False)