from flask import Flask, current_app
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    from webapp import services
    from webapp import models
    from webapp import controllers
    app = Flask(__name__)
    app.config.from_object("config.Config")
    models.init_app(app)
    controllers.init_app(app)
    handler = RotatingFileHandler(app.root_path + app.config["LOGGING_FILE_PATH"],
                                  maxBytes=10*1024*1024, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-8s %(message)s'))
    app.logger.addHandler(handler)

    return app
