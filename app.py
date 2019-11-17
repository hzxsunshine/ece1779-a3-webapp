from webapp import create_app
from flask import session
from datetime import timedelta

app = create_app()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=25)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
