from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.widgets import TextArea
from wtforms import validators
from webapp.repository import voteRepository


class CreateVoteForm(FlaskForm):
    vote_topic = StringField('Vote Topic', widget=TextArea(), validators=[validators.DataRequired(), validators.Length(min=2, max=500)])
    option1 = StringField('Option 1', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option2 = StringField('Option 2', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option3 = StringField('Option 3', validators=[validators.DataRequired(), validators.Length(min=2, max=200)])
    option4 = StringField('Option 4', validators=[validators.optional(), validators.Length(min=2, max=200)])
    option5 = StringField('Option 5', validators=[validators.optional(), validators.Length(min=2, max=200)])

    submit = SubmitField('Post Vote')


def create_vote(username, vote_form):
    return voteRepository.create_vote(username, vote_form)
