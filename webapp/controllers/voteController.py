from flask import Blueprint, render_template, redirect, url_for, request, session, current_app
from webapp.services import voteService
from webapp.services import userService
from decimal import Decimal

votes = Blueprint('votes', __name__)

VOTE_CREATION_PAGE = "vote.creation.html"
VOTE_LIST_PAGE = "votes.list.html"
MY_VOTE_LIST_PAGE = "myvotes.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."
LOGIN_PAGE = "login.html"


@votes.route('/vote', methods=['GET', 'POST'])
def post_vote():
    if 'username' not in session:
        login_form = userService.LoginForm()
        error = "To initiate a vote, you need to login to your account first!"
        return render_template(LOGIN_PAGE, title='Login', form=login_form, error=error)
    form = voteService.CreateVoteForm()
    if form.validate_on_submit():
        vote_id = voteService.create_vote(username=session['username'], vote_form=form)
        message = "Vote with id : " + vote_id + " has been initiated successfully!"
        return render_template(VOTE_CREATION_PAGE, title='Post Vote', form=form, message=message)
    else:
        if request == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(VOTE_CREATION_PAGE, title='Post Vote', form=form, error=INTERNAL_ERROR_MSG), 500

    return render_template(VOTE_CREATION_PAGE, title='Post Vote', form=form)


@votes.route('/hotvotes', methods=['GET'])
def hot_vote():
    login = True
    if 'username' not in session:
        login = False
    (all_vote_list, hot_votes) = voteService.list_all_vote()
    return render_template("votes.hot.html", login=login, title='Hot Topics', hot_votes=hot_votes)


@votes.route('/listallvotes', methods=['GET', 'POST'])
def list_vote():
    login = True
    if 'username' not in session:
        login = False
    (all_vote_list, hot_votes) = voteService.list_all_vote()
    form = voteService.SearchForm()
    if form.validate_on_submit():
        results = voteService.search_votes(search_form=form)
        message = str(len(results)) + ' result found from searching!'
        return render_template(VOTE_LIST_PAGE, login=login, title="Search Topics",
                               form=form, votes=all_vote_list, hot_votes=hot_votes, votesPosted=results, message=message)  # render_template(VOTE_CREATION_PAGE, title='Search Results', form=form)
    else:
        if request == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(VOTE_LIST_PAGE, login=login, title='Search Topics', form=form, votes=all_vote_list, hot_votes=hot_votes, error=INTERNAL_ERROR_MSG), 500

    return render_template(VOTE_LIST_PAGE, login=login, title='Search Topics', form=form, votes=all_vote_list, hot_votes=hot_votes)


@votes.route('/listmyvotes', methods=['GET'])
def list_my_vote():
    if 'username' not in session:
        login_form = userService.LoginForm()
        error = "To see your vote topics, you need to login to your account first!"
        return render_template(LOGIN_PAGE, title='Login', form=login_form, error=error)
    posted_votes = voteService.list_posted_votes(session['username'])
    voted_votes = voteService.list_voted_votes(session['username'])
    return render_template(MY_VOTE_LIST_PAGE, title='List My Vote', votesPosted=posted_votes, votesVoted=voted_votes)


@votes.route('/votes.detail/<vote_id>/<vote_create_time>', methods=['GET', 'POST'])
def vote_details(vote_id, vote_create_time):
    # post = voteService.list_specific_vote(vote_id, vote_create_time)
    post = voteService.list_specific_vote(vote_id)
    if 'username' in session:
        username = session['username']
        ID = voteService.list_voted_IDS(username)
        if vote_id in ID:
            return redirect(url_for('votes.vote_results', vote_id=vote_id, vote_create_time=vote_create_time))

    post_topic = post["topic"]
    options = post["options"]
    option1 = options[0]["content"] # option1
    option2 = options[1]["content"] # option2
    option3 = options[2]["content"] # option3
    try:
        option4 = options[3]["content"] # option 4
    except IndexError:
        option4 = []
    try:
        option5 = options[4]["content"] # option 5
    except IndexError:
        option5 = []

    if request.method == 'POST':
        if 'username' not in session:
            login_form = userService.LoginForm()
            error = "To involve in a vote, you need to login to your account first!"
            return render_template(LOGIN_PAGE, title='Login', form=login_form, error=error)
        if request.form.get('name') is None:
            error = "You need to select one option!"
            return render_template('votes.detail.html', vote_id=vote_id, vote_create_time=vote_create_time,
                                   topic=post_topic,
                                   options=options,
                                   option1=option1, option2=option2, option3=option3, option4=option4, option5=option5,
                                   error=error)
        num = int(request.form.get('name'))

        username = session['username']
        ID = voteService.list_voted_IDS(username)

        if vote_id in ID:
            return redirect(url_for('votes.vote_results', vote_id=vote_id, vote_create_time=vote_create_time))
        else:
            voteService.vote_update(vote_id, num)
            userService.update_user_votes(username, vote_id)
            return redirect(url_for('votes.vote_results', vote_id=vote_id,vote_create_time=vote_create_time))

    return render_template('votes.detail.html', vote_id=vote_id, vote_create_time=vote_create_time, topic=post_topic, options=options,
                           option1 = option1, option2 = option2, option3 = option3, option4 = option4,
                           option5 = option5)


@votes.route('/votes.result/<vote_id>/<vote_create_time>', methods=['GET','POST'])
def vote_results(vote_id, vote_create_time):
    if 'username' not in session:
        return redirect(url_for('votes.vote_details', vote_id = vote_id, vote_create_time = vote_create_time))

    post = voteService.list_specific_vote(vote_id)
    username = session['username']
    ids = voteService.list_voted_IDS(username)

    if vote_id not in ids:
        return redirect(url_for('votes.vote_details', vote_id=vote_id, vote_create_time=vote_create_time))

    post_topic = post["topic"]
    options = post["options"]
    sum_all = 0
    for i in range(len(options)):
        sum_all += int(options[i]['counts']) * 0.01
    fractions = []
    for i in range(len(options)):
        fractions.append(int(int(options[i]['counts'])/sum_all * 100 + 0.5)/ 100.0)

    option1 = options[0] # option1
    option2 = options[1] # option2
    option3 = options[2] # option3
    try:
        option4 = options[3] # option 4
    except IndexError:
        option4 = []
    try:
        option5 = options[4] # option 5
    except IndexError:
        option5 = []

    return render_template('votes.result.html', vote_id=vote_id, vote_create_time=vote_create_time, topic=post_topic,
                           options=options, fractions=fractions,
                           option1=option1, option2=option2, option3=option3, option4=option4,
                           option5=option5)

