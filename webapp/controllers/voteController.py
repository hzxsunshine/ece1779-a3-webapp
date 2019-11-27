from flask import Blueprint, render_template, redirect, url_for, request, session, current_app
from webapp.services import voteService
from webapp.services import userService
from decimal import Decimal

votes = Blueprint('votes', __name__)

VOTE_CREATION_PAGE = "vote.creation.html"
VOTE_LIST_PAGE = "votes.list.html"
MY_VOTE_LIST_PAGE = "myvotes.html"
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


@votes.route('/search', methods=['GET', 'POST'])
def search_vote():
    form = voteService.SearchForm()
    if form.validate_on_submit():
        results = voteService.search_votes(search_form = form)
        return render_template('votes.search.html', title=results, form=form) #render_template(VOTE_CREATION_PAGE, title='Search Results', form=form)
    else:
        if request == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template('votes.search.html', title='search', form=form, error=INTERNAL_ERROR_MSG), 500

    return render_template('votes.search.html', title='Search', form=form)


@votes.route('/listallvotes', methods=['GET'])
def list_vote():
    login = True
    if 'username' not in session:
        login = False
    all_vote_list = voteService.list_all_vote()
    return render_template(VOTE_LIST_PAGE, login=login, title='List Vote', votes=all_vote_list)


@votes.route('/listmyvotes', methods=['GET'])
def list_my_vote():
    if 'username' not in session:
        return redirect(url_for('users.login'))
    posted_votes = voteService.list_posted_votes(session['username'])
    voted_votes = voteService.list_voted_votes(session['username'])
    return render_template(MY_VOTE_LIST_PAGE, title='List My Vote', votesPosted=posted_votes, votesVoted=voted_votes)

@votes.route('/votes.detail/<voteID>/<vote_create_time>', methods=['GET','POST'])
def vote_details(voteID, vote_create_time):
    # post = voteService.list_specific_vote(voteID, vote_create_time)
    post = voteService.list_specific_vote(voteID)
    if 'username' in session:
        username = session['username']
        ID = voteService.list_voted_IDS(username)
        if Decimal(voteID) in ID:
            return redirect(url_for('votes.vote_results', voteID=voteID, vote_create_time=vote_create_time))


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
            return redirect(url_for('users.login'))
        num = int(request.form.get('name'))

        username = session['username']
        ID = voteService.list_voted_IDS(username)

        if Decimal(voteID) in ID:
            return redirect(url_for('votes.vote_results', voteID=voteID, vote_create_time=vote_create_time))
        else:
            #voteService.vote_update(voteID, vote_create_time, num)
            voteService.vote_update(voteID, num)
            userService.update_user_votes(username,voteID)
            return redirect(url_for('votes.vote_results', voteID=voteID,vote_create_time=vote_create_time))

    return render_template('votes.detail.html', voteID=voteID, vote_create_time=vote_create_time, topic=post_topic, options=options,
                           option1 = option1, option2 = option2, option3 = option3, option4 = option4,
                           option5 = option5)


@votes.route('/votes.result/<voteID>/<vote_create_time>', methods=['GET','POST'])
def vote_results(voteID, vote_create_time):
    if 'username' not in session:
        return redirect(url_for('votes.vote_details', voteID = voteID, vote_create_time = vote_create_time))

    post = voteService.list_specific_vote(voteID)
    #post = voteService.list_specific_vote(voteID, vote_create_time)
    username = session['username']
    IDs = voteService.list_voted_IDS(username)

    if Decimal(voteID) not in IDs:
        return redirect(url_for('votes.vote_details', voteID = voteID, vote_create_time = vote_create_time))

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

    return render_template('votes.result.html', voteID=voteID, vote_create_time=vote_create_time, topic=post_topic, options = options, fractions = fractions,
                           option1 = option1, option2 = option2, option3 = option3, option4 = option4,
                           option5 = option5)

