from datetime import timedelta


class Config(object):
    DEBUG = True
    LOGGING_FILE_PATH = "/ece1779.log"
    TESTING = False
    SECRET_KEY = "fe8e5c349e8eb13bf65bdc261229d43d"

    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "mysql://ece1779a2:password123@ece1779a2-rds.coc6d8upfz6v.us-east-1.rds.amazonaws.com/ece1779a2"

    REMEMBER_COOKIE_DURATION = timedelta(hours=25)
    S3_BUCKET_LOCATION = "https://2019fall-ece1779a2.s3.amazonaws.com/"
    S3_BUCKET_NAME = "2019fall-ece1779a2"

