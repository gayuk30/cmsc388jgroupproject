from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import email_validator

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class JobForm(FlaskForm):
    company = StringField('Company', validators=[InputRequired()])
    position = StringField('Position', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    stars = SelectField('Stars', choices=[(str(i), str(i)) for i in range(6)], validators=[InputRequired()])
    review = TextAreaField('Review')
    submit = SubmitField('Submit')