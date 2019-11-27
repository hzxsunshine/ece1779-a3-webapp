from flask import current_app
import uuid
from datetime import datetime
import decimal
from boto3.dynamodb.types import DYNAMODB_CONTEXT
from boto3.dynamodb.conditions import Key
import re
import json

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

def search_votes(search_form):
    keywords = search_form.data
    dynamodb = current_app.extensions['dynamo']

    # keyword = re.sub('  ', " ", re.sub("[\u0060|\u0021-\u002c|\u002e-\u002f|\u003a-\u003f|\u2200-\u22ff|\uFB00-\uFFFD|\u2E80-\u33FF]", ' ', keywords)).split(' ')
    # words = json.dump(keyword)

    results = dynamodb.tables['votes'].scan(
        FilterExpression=Attr("topic").eq("test")
    )
    return results["Items"]


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
    IDs = list_voted_ID(username)

    votes = []
    for voteID in IDs:
        voteID = convertID(voteID)
        vote = dynamodb.tables['votes'].get_item(Key={'id': voteID})

        if 'Item' in vote:
            votes.append(vote['Item'])
    return votes


def list_voted_ID(username):
    dynamodb = current_app.extensions['dynamo']
    response = dynamodb.tables['users'].get_item(
      Key={
        'username': username
      }
    )
    voteIDs = []
    if 'Item' in response:
        item =  response['Item']
        for n in item['votes_involved_in']:
            voteIDs.append(n)
    return voteIDs

# list a specific vote:
#def list_specific_vote(voteID, vote_create_time):
def list_specific_vote(voteID):
    dynamodb = current_app.extensions['dynamo']
    ID = convertID(voteID)
    #response = dynamodb.tables['votes'].get_item(Key={'id': ID, 'create_time':vote_create_time})
    response = dynamodb.tables['votes'].get_item(Key={'id': ID})
    if 'Item' in response:
        return response['Item']
    else:
        return []


def convertID(voteID):
    try:
        ID = int(voteID)
    except ValueError:
        ID = int(voteID[:-4].replace('.',''))
    if len(str(ID)) < 39:
        ID = int(str(ID) + '0' * (39 - len(str(ID))))
    return ID

#def update_vote(voteID, vote_create_time, optionID):
def update_vote(voteID, optionID):
    ID = convertID(voteID)
    dynamodb = current_app.extensions['dynamo']
    # response = dynamodb.tables['votes'].get_item(Key={'id': ID, 'create_time':vote_create_time})
    response = dynamodb.tables['votes'].get_item(Key={'id': ID})

    #update = str(int(response['Item']["options"][int(optionID)]["count"]) + 1)
    dynamodb.tables['votes'].update_item(
        Key={
            'id': ID,
            # 'create_time': vote_create_time
        },
        # UpdateExpression= 'set #ctr = #ctr + :val',
        UpdateExpression='set options[{}].counts = options[{}].counts + :val'.format(optionID,optionID),
        # ExpressionAttributeNames={"#ctr": "options[1].count"},
        ExpressionAttributeValues={
            ':val': decimal.Decimal(1)
        }
    )



