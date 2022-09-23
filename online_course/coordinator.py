from .imports import *
from .models import *
import os
from uuid import uuid4


coordinator = Blueprint('app_coordinator', __name__, url_prefix = '/coordinator', template_folder = 'templates')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','mp4', 'flv', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def make_unique(string):
    ident = uuid4().__str__()[:16]
    return f'{ident}-{string}'


@coordinator.route('/new-course', methods=['GET', 'POST'])
def index():
    user = session.get('user', None)
    UPLOAD_FOLDER2 = current_app.config['UPLOAD_FOLDER']    
    VIDEO_FOLDER2 = current_app.config['VIDEO_FOLDER']

    if request.method =='POST':
        title = request.form['title']
        details = request.form['details']
        service = request.form['service']
        img_link = request.files['file']
        video_link = request.files['video']

        if title and details and service and img_link and video_link and request.method =='POST':

            
            if 'file' and 'video' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            video = request.files['video']
        
            if file.filename == '' and video.filename =='':
                flash('No selected file')
                return redirect(request.url)
            if file and video and allowed_file(file.filename) and allowed_file(video.filename):
                filename = secure_filename(file.filename)
                videoname = secure_filename(video.filename)
                unique_img = make_unique(filename)
                unique_video = make_unique(videoname)
                file.save(os.path.join(UPLOAD_FOLDER2, unique_img))
                video.save(os.path.join(VIDEO_FOLDER2, unique_video))

                new_course = Course(title, details, service ,unique_img, unique_video)
                db.session.add(new_course)
                db.session.commit()

                flash('Upload successful!')
                return redirect(url_for('app_coordinator.index'))

    extensions = ExtensionService.query.all()
    return render_template('coordinator_index.html', user = user , extensions = extensions)

@coordinator.route('/advertisement', methods = ['GET', 'POST'])
def advertisement():
    pass


@coordinator.route('/add-new-service', methods = ['GET', 'POST'])
def new_service():
    user = session.get('user', None)
    UPLOAD_FOLDER = os.path.join(current_app.config['EXTENSIONS_FOLDER'])
    form = NewServiceForm()

    if form.validate_on_submit():

        f = form.logo.data
        file = secure_filename(f.filename)
        unique_logo = make_unique(file)
        f.save(os.path.join(UPLOAD_FOLDER, unique_logo))
        new_service =ExtensionService(form.title.data, form.details.data, unique_logo)
        db.session.add(new_service)
        db.session.commit()
        flash('New extension service created!')
        return redirect(url_for('app_coordinator.new_service'))
    return render_template('new_service.html', user = user, form = form)


