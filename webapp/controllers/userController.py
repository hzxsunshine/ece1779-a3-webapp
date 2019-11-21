from flask import Blueprint, render_template, redirect, url_for, request, session
from webapp.services import userService
from flask import current_app


users = Blueprint('users', __name__)

LOGIN_PAGE = "login.html"
REGISTER_PAGE = "register.html"
INTERNAL_ERROR_MSG = "Internal Error, please try again later."
AUTHENTICATION_ERROR = "Login Unsuccessful. Please check username and password."
REG_SUCCESS_MSG = "Registration successful, please login."
USER_EXISTED_ERROR = "User with username '{}' already exists."


@users.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('main.home'))
    form = userService.LoginForm()
    if form.validate_on_submit():
        authenticated_user = userService.is_authenticated(username=form.username.data, password=form.password.data)
        if authenticated_user:
            session['username'] = form.username.data
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            current_app.logger.error("----------User '{}' Login failed, username/password do not match record----------"
                                     .format(form.username.data))
            return render_template(LOGIN_PAGE, title='Login', form=form, error=AUTHENTICATION_ERROR), 401
    else:
        if request == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(LOGIN_PAGE, title='Login', form=form, error=INTERNAL_ERROR_MSG), 500
    return render_template(LOGIN_PAGE, title='Login', form=form)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = userService.CreateUserForm()
    if 'username' in session:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        response = userService.get_user_by_username(username=form.username.data)
        user_with_username = None
        if 'Item' in response and 'username' in response['Item']:
            user_with_username = response['Item']['username']
        if user_with_username:
            current_app.logger.error("----------409 Registration conflict: {} already exists----------"
                                     .format(form.username.data))
            return render_template(REGISTER_PAGE, title='Register', form=form,
                                   error=USER_EXISTED_ERROR.format(form.username.data)), 409
        else:
            try:
                userService.create_user(username=form.username.data, password=form.password.data)
                login_form = userService.LoginForm()
                current_app.logger.info("----------User '{}' register successful----------".format(form.username.data))
                return render_template(LOGIN_PAGE, title='Login', form=login_form, message=REG_SUCCESS_MSG)
            except Exception as e:
                current_app.logger.error("----------Database action error: {}----------".format(str(e)))
                return render_template(REGISTER_PAGE, title='Register', form=form, error=INTERNAL_ERROR_MSG), 500
    else:
        if request.method == 'POST':
            current_app.logger.error("----------Internal Error: {}----------".format(form.errors))
            return render_template(REGISTER_PAGE, title='Register', form=form, error=INTERNAL_ERROR_MSG), 500
    return render_template(REGISTER_PAGE, title='Register', form=form)


@users.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('users.login'))
