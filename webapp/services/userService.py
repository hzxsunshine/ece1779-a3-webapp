from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from webapp.repository import userRepository
from werkzeug import security


class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember_user = BooleanField('Remember Me')
    submit = SubmitField('Login')


def get_user_by_username(username):
    return userRepository.get_user_by_username(username)


def is_authenticated(username, password):
    response = userRepository.get_user_by_username(username)
    if 'Item' in response and 'username' in response['Item'] and security.check_password_hash(response['Item']['password'], password):
        print(response['Item']['username'])
        return response['Item']['username']
    else:
        return None


def create_user(username, email, password):
    hashed_password = security.generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
    userRepository.create_user(username, email, hashed_password)


def update_user_votes(username, vote_id):
    return userRepository.update_user_votes(username, vote_id)



