from flask import Blueprint
from flask import redirect, url_for

main = Blueprint('main', __name__)


@main.route('/')
def home():
    return redirect(url_for('users.login'))
