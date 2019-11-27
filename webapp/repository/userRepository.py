from flask import current_app
from decimal import Decimal


def get_user_by_username(username):
    dynamodb = current_app.extensions['dynamo']
    return dynamodb.tables['users'].get_item(
      Key={
        'username': username
      }
    )


def create_user(username, email, password):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['users'].put_item(
      Item={
        'username': username,
        'email': email,
        'password': password,
        'votes_involved_in': [],
      })

    print(response)


def update_user_votes(username, vote_id):
    dynamodb = current_app.extensions['dynamo']
    dynamodb.tables['users'].update_item(
        Key={
            'username': username
        },
        UpdateExpression='set votes_involved_in = list_append(votes_involved_in, :val)',
        ExpressionAttributeValues={
            ':val': [vote_id]
        }
    )
    return True
