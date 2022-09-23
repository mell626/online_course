from .imports import * 
from .models import *
import os
from functools import cache


course = Blueprint('app_course', __name__, url_prefix= '/course', template_folder = 'templates')


@cache
@course.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        _datestamp = request.json
        _date = _datestamp['link']

        if _date and request.method == 'POST':
            return jsonify({'data': _date})
            
    if not 'user' in session:
        flash('Login or signup to access our free webinars and courses.')

    user = session.get('user', None)
    data = Course.query.limit(12).all()
    return render_template('course_index.html', user = user, data = data)


@cache
@course.route('/watch/<string:link>')
def watch(link):
    user = session.get('user',None)
    if 'user' in session:
        course  = Course.query.filter_by(id = link).first()
        if course:
            return render_template('watch.html', course = course, user = user)
    return redirect(url_for('app_user.login'))


@course.route('/view', methods =['GET', 'POST'])
def view():
    if 'user' in session:
        user = session.get('user', None)

        return render_template('course_view.html', user = user)
    flash('You must login to continue')
    return redirect(url_for('app_user.login'))