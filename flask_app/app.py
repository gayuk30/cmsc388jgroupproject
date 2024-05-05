from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import certifi
import os
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm, ProjectForm, ReviewForm    
from models import User

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://yer:HUtySU4t80h55iXJ@cluster0.vz6chxl.mongodb.net/Cluster0?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = str(os.urandom(16))

mongo = PyMongo(app, tlsCAFile=certifi.where())

login_manager = LoginManager(app)
login_manager.login_view = 'login'

users = Blueprint("users", __name__)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def hello_world():
    return 'Hello'


@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = mongo.db.users.find_one({'username': username, 'password': password})
        if user:
            # User found, log them in and redirect to reviews page
            login_user(User(username))
            return redirect(url_for('reviews'))
        else:
            # User not found, display an error message
            return render_template('login.html', form=form, error='Invalid username or password')
    return render_template('login.html', form=form)



@users.route('/register', methods = ['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if mongo.db.users.find_one({'username': username}) is not None:
            return render_template('register.html', form=form, error='Username already exists, try logging in.')
        else:
            mongo.db.users.insert_one({'username': username, 'password': password})
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


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
    form = ReviewForm()
    if current_user.is_authenticated:
        # User is logged in, pass the username into the template so when they leave a review, it will be associated with their username
        return render_template('/reviews.html', username=current_user.username, logged_in=True, form=form)
    else:
        # If the user is not logged in, they can still view the reviews page, they just cannot leave a review
        return render_template('/reviews.html', logged_in=False)