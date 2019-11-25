from flask import current_app
from decimal import Decimal


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
      Item={
        'username': username,
        'password': password,
        'votes_involved_in': [],
      })

    print(response)

def convertID(voteID):
    try:
        ID = int(voteID)
    except ValueError:
        ID = int(voteID[:-4].replace('.',''))
    if len(str(ID)) < 39:
        ID = int(str(ID) + '0' * (39 - len(str(ID))))
    return ID

def update_user_votes(username, voteID):
    dynamodb = current_app.extensions['dynamo']
    ID = convertID(voteID)
    dynamodb.tables['users'].update_item(
        Key={
            'username': username
        },
        UpdateExpression='set votes_involved_in = list_append(votes_involved_in, :val)',
        ExpressionAttributeValues={
            ':val': [Decimal(ID)]
        }
    )
    return True
