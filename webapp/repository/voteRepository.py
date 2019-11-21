from flask import current_app
import uuid
from datetime import datetime
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key
# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0


def create_vote(username, vote_form):
    options = [dict(content=vote_form.option1.data, count=0),
               dict(content=vote_form.option2.data, count=0),
               dict(content=vote_form.option3.data, count=0)]

    if vote_form.option4.data is not None and vote_form.option4.data != "":
        options.append(dict(content=vote_form.option4.data, count=0))
    if vote_form.option5.data is not None and vote_form.option5.data != "":
        options.append(dict(content=vote_form.option5.data, count=0))

    vote_id = uuid.uuid1().int
    dynamodb = current_app.extensions['dynamo']
    dynamodb.tables['votes'].put_item(
      Item={
        'id': vote_id,
        'create_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'username': username,
        'topic': vote_form.vote_topic.data,
        'options': options
      })
    return vote_id


# when user involves other people's vote, use the code below:

# dynamodb.tables['users'].update_item(
#       Key={
#         'username': username
#       },
#       UpdateExpression="SET votes_involved_in = list_append(votes_involved_in, :i)",
#       ExpressionAttributeValues={
#         ':i': [vote_id],
#       },
#       ReturnValues="UPDATED_NEW"
#     )

def list_all_vote():
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['votes'].scan()
    if "Items" in response:
        return response["Items"]
    else:
        return []


def list_posted_votes(username):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['votes'].query(
        IndexName="userIndex",
        KeyConditionExpression = Key('username').eq(username)
    )
    if 'Items' in response:
        return response["Items"]
    else:
        return []


def list_voted_votes(username):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['users'].get_item(
      Key={
        'username': username
      }
    )
    if "votes_involved_in" in response:
        votes = []
        for voteID in response['votes_involved_in']:
            vote = dynamodb.tables['votes'].get_item(Key={'id': voteID})
            if 'Item' in vote:
                votes.append(vote['Item'])
        return votes
    else:
        return []