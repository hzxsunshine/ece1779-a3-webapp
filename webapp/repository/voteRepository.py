from flask import current_app
import uuid
from datetime import datetime
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from boto3.dynamodb.conditions import Or
import re
import json
from boto3 import dynamodb

# Inhibit Inexact Exceptions
DYNAMODB_CONTEXT.traps[decimal.Inexact] = 0
# Inhibit Rounded Exceptions
DYNAMODB_CONTEXT.traps[decimal.Rounded] = 0


def create_vote(username, vote_form):
    options = [dict(content=vote_form.option1.data, counts=0),
               dict(content=vote_form.option2.data, counts=0),
               dict(content=vote_form.option3.data, counts=0)]

    if vote_form.option4.data is not None and vote_form.option4.data != "":
        options.append(dict(content=vote_form.option4.data, counts=0))
    if vote_form.option5.data is not None and vote_form.option5.data != "":
        options.append(dict(content=vote_form.option5.data, counts=0))

    vote_id = str(uuid.uuid4())
    dynamodb = current_app.extensions['dynamo']
    dynamodb.tables['votes'].put_item(
      Item={
        'id': vote_id,
        'create_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'username': username,
        'topic': vote_form.vote_topic.data,
        'options': options,
        'valid_days': vote_form.valid_days.data,
        'num_voted': 0
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

def search_votes(search_form):
    keywords = search_form.vote_topic.data
    dynamodb = current_app.extensions['dynamo']

    keyword = re.sub('  ', " ", re.sub("[\u0060|\u0021-\u002c|\u002e-\u002f|\u003a-\u003f|\u2200-\u22ff|\uFB00-\uFFFD|\u2E80-\u33FF]",
                                       ' ', keywords)).split(' ')
    filter_expression_list = []

    while("" in keyword):
        keyword.remove("")


    if len(keyword) > 1:
        for i in range(len(keyword)):
            filter_expression_list.append(Attr("topic").contains("{}".format(keyword[i])))

        expression = Or(*filter_expression_list)
    elif len(keyword) == 1:
        expression = Attr("topic").contains("{}".format(keyword[0]))
    else:
        return False

    results = dynamodb.tables['votes'].scan(
        FilterExpression = expression
    )
    return results["Items"]


def list_all_vote():
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['votes'].scan()
    if "Items" in response:
        hot_votes = find_hot_votes((response["Items"]))
        return (sort_votes(response["Items"]), hot_votes)
    else:
        return []


def list_posted_votes(username):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['votes'].query(
        IndexName="userIndex",
        KeyConditionExpression = Key('username').eq(username)
    )
    if 'Items' in response:
        return sort_votes(response["Items"])
    else:
        return []


def list_voted_votes(username):
    dynamodb = current_app.extensions['dynamo']
    IDs = list_voted_ID(username)

    votes = []
    for vote_id in IDs:
        vote = dynamodb.tables['votes'].get_item(Key={'id': vote_id})

        if 'Item' in vote:
            votes.insert(0, vote['Item'])
    return votes


def list_voted_ID(username):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['users'].get_item(
      Key={
        'username': username
      }
    )
    vote_ids = []
    if 'Item' in response:
        item = response['Item']
        for n in item['votes_involved_in']:
            vote_ids.append(n)
    return vote_ids


# list a specific vote:
def list_specific_vote(vote_id):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['votes'].get_item(Key={'id': vote_id})
    if 'Item' in response:
        return response['Item']
    else:
        return []


def find_hot_votes(votes):
    hot_votes = sorted(votes, key=lambda i: i['num_voted'], reverse=True)
    if len(hot_votes) >= 3:
        return hot_votes[0:3]
    else:
        return hot_votes


def update_vote(vote_id, option_id):
    dynamodb = current_app.extensions['dynamo']
    dynamodb.tables['votes'].get_item(Key={'id': vote_id})
    dynamodb.tables['votes'].update_item(
        Key={
            'id': vote_id,
        },
        UpdateExpression='set options[{}].counts = options[{}].counts + :val'.format(option_id,option_id),
        ExpressionAttributeValues={
            ':val': decimal.Decimal(1)
        }
    )

    dynamodb.tables['votes'].update_item(
        Key={
            'id': vote_id,
        },
        UpdateExpression='set num_voted = num_voted + :val',
        ExpressionAttributeValues={
            ':val': decimal.Decimal(1)
        }
    )


def sort_votes(votes):
    return sorted(votes, key = lambda i: i['create_time'], reverse = True)
