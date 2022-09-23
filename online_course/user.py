from ast import Return
from .imports import *
from .models import *


user = Blueprint('app_user', __name__, url_prefix='/user', template_folder = 'templates')


@user.route('/login', methods = ['GET', 'POST'])
def login():

    if 'user' in session:
        flash('Already logged in')
        return redirect(url_for('default'))

    form = LoginForm()

    if form.validate_on_submit():
        log_user = User.query.filter_by(email = form.email.data).first()
        if log_user:
            pwd = log_user.password_hash
            pwd2 = form.password.data
            if check_password_hash(pwd, pwd2) == True:
                session['user'] = form.email.data
                flash('You are now logged in as ' + form.email.data)
                return redirect(url_for('default', user = form.email.data))

        flash('Invalid username or password!')
    return render_template('login.html', form = form)


@user.route('/reset-password', methods = ['GET', 'POST'])
@limiter.limit('10 per day')
def reset_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        account = User.query.filter_by(email = form.email.data).first()
        if account:
            return redirect(url_for('app_user.new_password', data = account))
    return render_template('forgot_password.html', form = form)


@user.route('/new-password/<data>', methods = ['GET', 'POST'])
def new_password(data):
    form = NewPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = data).first()

        candidate_pwd = str(form.password.data)
        print(candidate_pwd)

        if user:
            user.set_password = candidate_pwd
            db.session.commit()
            return '<h1>Password changed successfully! </h1>'
    return render_template('new_password.html', form = form)


@user.route('/signup', methods =['POST', 'GET'])
def signup():
    if 'user' in session:
        return redirect(url_for('default'))
    form = SignupForm()
    if form.validate_on_submit():
        
        new_user = User(email = form.email.data, password_hash =  generate_password_hash(form.password.data),last_name = form.last_name.data, first_name =  form.first_name.data, middle_name = form.middle_name.data)
        db.session.add(new_user)
        db.session.commit()
        return '<h3>Verify email<h/3>'

    return render_template('signup.html', form = form)


@user.route('/profile')
def profile():
    user = session.get('user', None)
    if 'user' in session:
        profile = User.query.filter_by(email = user).first()

        return render_template('profile.html', profile = profile, user = user)
    return redirect(url_for('default'))

@user.route('/logout')
def logout():
    session.clear()
    flash('You are logged out')
    return redirect(url_for('default'))

