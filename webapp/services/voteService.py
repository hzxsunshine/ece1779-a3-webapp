from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.widgets import TextArea
from wtforms import validators
from webapp.repository import voteRepository


class CreateVoteForm(FlaskForm):
    vote_topic = StringField('* Vote Topic', widget=TextArea(), validators=[validators.DataRequired(), validators.Length(min=2, max=500)])
    option1 = StringField('* Option 1: ', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option2 = StringField('* Option 2: ', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option3 = StringField('* Option 3: ', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option4 = StringField('Option 4: ', validators=[validators.optional(), validators.Length(min=2, max=200)])
    option5 = StringField('Option 5: ', validators=[validators.optional(), validators.Length(min=2, max=200)])
    valid_days = IntegerField('* vote will close in (days): ', validators=[validators.DataRequired(), validators.NumberRange(min=1, max=365)])

    submit = SubmitField('Post Vote')

class SearchForm(FlaskForm):
    vote_topic = StringField('Vote Topic', widget=TextArea(), validators=[validators.DataRequired(), validators.Length(min=1, max=500)])
    submit = SubmitField('Search')


def search_votes(search_form):
    return voteRepository.search_votes(search_form)

def create_vote(username, vote_form):
    return voteRepository.create_vote(username, vote_form)


def list_all_vote():
    return voteRepository.list_all_vote()


def list_posted_votes(username):
    return voteRepository.list_posted_votes(username)


def list_voted_votes(username):
    return voteRepository.list_voted_votes(username)


# def list_specific_vote(vote_id, vote_create_time):
#     return voteRepository.list_specific_vote(vote_id, vote_create_time)

def list_specific_vote(vote_id):
    return voteRepository.list_specific_vote(vote_id)

# def vote_update(vote_id, vote_create_time, option_id):
#     return voteRepository.update_vote(vote_id, vote_create_time, option_id)

def vote_update(vote_id,option_id):
    return voteRepository.update_vote(vote_id, option_id)


def list_voted_IDS(username):
    return voteRepository.list_voted_ID(username)
