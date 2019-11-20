from .mainController import *
from .userController import *
from .voteController import *


def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(votes)
    return app
