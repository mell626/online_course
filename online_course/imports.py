from flask import *
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
import email_validator
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from wtforms.widgets import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_user


db = SQLAlchemy()

migrate = Migrate()

limiter = Limiter(key_func = get_remote_address, storage_uri = 'memory://', default_limits = ['500 per day', '100 per hour'])

security = Security()
