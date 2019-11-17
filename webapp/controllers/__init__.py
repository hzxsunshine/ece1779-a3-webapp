from .mainController import *
from .userController import *


def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(users)
    return app
