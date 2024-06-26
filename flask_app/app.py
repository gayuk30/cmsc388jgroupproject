from flask import Blueprint, Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import certifi
import os
from flask_wtf import FlaskForm
from forms import RegistrationForm, LoginForm, JobForm, ReviewForm    
from models import User
from flask_bcrypt import Bcrypt
import requests


app = Flask(__name__)
app.config['GOOGLE_MAPS_API_KEY'] = os.getenv('GOOGLE_MAPS_API_KEY')
app.config['MONGO_URI'] = 'mongodb+srv://yer:HUtySU4t80h55iXJ@cluster0.vz6chxl.mongodb.net/Cluster0?retryWrites=true&w=majority&appName=Cluster0'
app.config['SECRET_KEY'] = str(os.urandom(16))

mongo = PyMongo(app, tlsCAFile=certifi.where())

login_manager = LoginManager(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)



users = Blueprint("users", __name__)
employer = Blueprint("employer", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/')
def profile():
    jobs = mongo.db.jobs.find({})
    # gmaps = googlemaps.Client(key='AIzaSyBka3GVX6IKfl4keozx5qTMpiRgpxusc9k')
    # map = KeplerGl(height=600, width=800)
    # map.add_data(data=jobs, name='jobs')
    # return map._repr_html_()
    waypoints = []
    for job in jobs:
        waypoints.append({'lat': float(job['latitude']), 'lng': float(job['longitude'])})

    jobs = mongo.db.jobs.find({})
    return render_template('profile.html', jobs=jobs, waypoints=waypoints)


if __name__ == '__main__':
    app.run(debug=True)

@users.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = mongo.db.users.find_one({'username': username})
        print(user)
        if user and bcrypt.check_password_hash(user['password'], password):
            # User found, log them in and redirect to reviews page
            login_user(User(username))
            return redirect(url_for('profile'))
        else:
            # User not found, display an error message
            return render_template('login.html', form=form, error='Invalid username or password')
    return render_template('login.html', form=form)

@users.route('/register', methods = ['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if mongo.db.users.find_one({'username': username}) is not None:
            return render_template('register.html', form=form, error='Username already exists, try logging in.')
        else:
            mongo.db.users.insert_one({'username': username, 'password': hashed_password})
            return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('profile'))

app.register_blueprint(users)

# done

@employer.route('/job', methods = ['GET', 'POST'])
def job():
    form = JobForm()
    if request.method == 'POST' and form.validate():
        company = form.company.data
        position = form.position.data
        description = form.description.data
        latitude = form.latitude.data
        longitude = form.longitude.data

        mongo.db.jobs.insert_one({
            'company': company,
            'position': position,
            'description': description,
            'latitude': latitude,
            'longitude': longitude
        })

        return redirect(url_for('profile'))

    return render_template('job.html', form=form)


@employer.route('/reviews', methods=['GET', 'POST'])
def reviews():
    reviews = mongo.db.reviews.find({})
    form = ReviewForm()
    if current_user.is_authenticated:
        return render_template('/reviews.html', username=current_user.username, logged_in=True, form=form, reviews=reviews)
    else:
        return render_template('/reviews.html', logged_in=False, reviews=reviews)


@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        stars = request.form['stars']
        comment = request.form['comment']

        mongo.db.reviews.insert_one({
            'stars': stars,
            'comment': comment,
            'username': current_user.username
        })

        return redirect(url_for('employer.reviews'))


app.register_blueprint(employer)