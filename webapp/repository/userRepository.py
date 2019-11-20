from flask import current_app


def get_user_by_username(username):
    dynamodb = current_app.extensions['dynamo']
    return dynamodb.tables['users'].get_item(
      Key={
        'username': username
      }
    )


def create_user(username, password):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['users'].put_item(
      data={
        'username': username,
        'password': password
      })
    print(response)
