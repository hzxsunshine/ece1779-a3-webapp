from webapp.models.user import User
from webapp.models.base import db


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def create_user(username, password):
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    return user
