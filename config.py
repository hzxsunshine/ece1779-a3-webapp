from datetime import timedelta


class Config(object):
    DEBUG = True
    LOGGING_FILE_PATH = "/ece1779.log"
    TESTING = False
    SECRET_KEY = "fe8e5c349e8eb13bf65bdc261229d43d"

    REMEMBER_COOKIE_DURATION = timedelta(hours=25)
    S3_BUCKET_LOCATION = "https://2019fall-ece1779a2.s3.amazonaws.com/"
    S3_BUCKET_NAME = "2019fall-ece1779a2"

    DYNAMO_TABLES = [
      {'TableName': 'users',
       'KeySchema': [dict(AttributeName='username', KeyType='HASH')],
       'AttributeDefinitions': [dict(AttributeName='username', AttributeType='S')],
       'ProvisionedThroughput': dict(ReadCapacityUnits=5, WriteCapacityUnits=5)
       }
    ]

    DYNAMO_ENABLE_LOCAL = True
    DYNAMO_LOCAL_HOST = 'localhost'
    DYNAMO_LOCAL_PORT = 8000

