from .imports import *
from .user import user
from .course import course
from .admin import *
from .service import service
from .coordinator import coordinator
import os
from .models import *


def create_app():
    app = Flask(__name__)

    IMG_FOLDER = os.path.join('./online_course/static/img')
    VIDEO_FOLDER = os.path.join('./online_course/static/video')
    VIDEO_FOLDER2 = os.path.join('static', 'video')
    EXTENSIONS_FOLDER = os.path.join('./online_course/static/ext')

    app.config['SECRET_KEY'] = '0defe7fc3d7929831b5c72956e45c6450ea762c8ad0ee49589a48771e619101243418f81ecfe772cc74139793f76b5401c1c1083505dcea3f40fec6e8f9d1adfc18aadf58b0f21f7bb8e29692756c63b88a3467363e61aa0864c01faa2f02ada87e7f6ff9e3fd930956b0050410bf76cb0fffd7e72c1fa4fab7a5635be99fc0a64fd432d40c758cb84647d910701c13ce84ed23a5e585bd73202970653e1db52bd56b98b4c81ca3777f7202e7dc896024b71e03ecc126adb4d119c916dda39655e322c5f4c8c91fafcadbca0bfb55f2c96a348dd296ce50ea175369343f8a6a74d5d830b20bc211ebbd604a1d2b2d4965a4e026f6d3dc2378d84b38cd677b146'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER
    app.config['VIDEO_FOLDER'] = VIDEO_FOLDER
    app.config['VIDEO_FOLDER2'] = VIDEO_FOLDER2
    app.config['EXTENSIONS_FOLDER'] = EXTENSIONS_FOLDER
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = 'a44c628a98132b184095c61c0d2ba0a4b39058241fea9ad25dce0045ea058e46'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    app.register_blueprint(user)
    app.register_blueprint(course)
    app.register_blueprint(service)
    app.register_blueprint(coordinator)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)


    db.init_app(app)
    admin.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    security.init_app(app, user_datastore)


    @app.before_first_request
    def create_super_user():
        # db.drop_all()
        # db.session.commit()
        db.create_all(app=create_app())
        if not security.datastore.find_user(email = 'me@gmail.com'):
            security.datastore.create_user(email = 'me@gmail.com', password_hash = generate_password_hash('flask is the best'))
            db.session.commit()


    @app.route('/')
    def default():        
        user = session.get('user', None)
        
        return render_template('default.html', user = user)

    @app.route('/about')
    def about():
        return render_template('about.html')


    return app