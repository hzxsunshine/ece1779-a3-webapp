from flask import Blueprint, render_template, redirect, url_for, request, session, current_app
from webapp.services import voteService


votes = Blueprint('votes', __name__)

VOTE_CREATION_PAGE = "vote.creation.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."


@votes.route('/vote', methods=['GET', 'POST'])
def post_vote():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    form = voteService.CreateVoteForm()
    if form.validate_on_submit():
        vote_id = voteService.create_vote(username=session['username'], vote_form=form)
        return "Vote with id : " + str(vote_id) + "post successfully"
    else:
        if request == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(VOTE_CREATION_PAGE, title='Post Vote', form=form, error=INTERNAL_ERROR_MSG), 500

    return render_template(VOTE_CREATION_PAGE, title='Post Vote', form=form)
