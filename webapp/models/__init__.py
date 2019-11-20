from flask_dynamo import Dynamo


def init_app(app):
    dynamo = Dynamo(app)
    dynamo.create_all()

    return app
