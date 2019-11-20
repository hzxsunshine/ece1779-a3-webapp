from flask import Blueprint, session
from flask import redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if 'username' in session:
        return session['username']
    else:
        return redirect(url_for('users.login'))
