from flask import Blueprint, session
from flask import redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('votes.list_my_vote'))
    else:
        return redirect(url_for('users.login'))
