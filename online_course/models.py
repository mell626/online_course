from email.policy import default
from enum import unique
from .imports import *
from datetime import datetime
import uuid



role_users = db.Table('role_users', db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    details = db.Column(db.String(255))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(40), default = uuid.uuid4().hex)
    email = db.Column(db.String(100), unique = True)
    password_hash = db.Column(db.String(300))
    active = db.Column(db.Boolean())
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    occupation = db.Column(db.Integer)
    adress = db.Column(db.Text)
    profile_pic = db.Column(db.String(200))
    date_verified = db.Column(db.DateTime)
    roles = db.relationship('Role', secondary=role_users,backref=db.backref('users', lazy='dynamic'))
    date_created = db.Column(db.DateTime, default = datetime.today())

    @property
    def password(self):
        return db.session.get(self.password_hash)

    @password.setter
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{ self.email }'


class ExtensionService(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(40), unique = True)
    title = db.Column(db.String(40))
    details = db.Column(db.Text)
    img_link = db.Column(db.String(255))
    status = db.Column(db.String(1), default ='a')
    courses = db.relationship('Course', backref = 'extension_service', lazy = True)
    date_created = db.Column(db.DateTime, default = datetime.today())

    def __init__(self, title, details, img_link):
        self.public_id = str(uuid.uuid4().hex)
        self.title = title
        self.details = details
        self.img_link = img_link

    def set_status(self, status):
        self.status = status

    def __repr__(self):
        return f'{self.title}'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(40), unique = True)
    title = db.Column(db.String(100))
    details = db.Column(db.Text)
    extension_service_id = db.Column(db.Integer, db.ForeignKey('extension_service.id'))
    img_link = db.Column(db.String(200))
    video_link = db.Column(db.String(200))
    ecertificate_link = db.Column(db.String(255))
    status = db.Column(db.String(1), default = 'i')
    date_created = db.Column(db.DateTime, default = datetime.today())


    def __init__(self, title, details, extension_service_id, img_link, video_link):
        self.public_id = str(uuid.uuid4().hex)
        self.title = title
        self.details = details
        self.extension_service_id = extension_service_id
        self.img_link = img_link
        self.video_link = video_link

    def set_status(self, status):
        self.status = status

    def __repr__(self):
        return f' { self.title } '





class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Must be a valid email.')], render_kw = {'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8, max = 255)])


class SignupForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email('Must be a valid email.')], render_kw = {'autofocus': True})
    password = PasswordField('Password:', validators = [DataRequired(), Length(min = 8, max = 255), EqualTo('confirm', message = 'Password must match!')])
    confirm = PasswordField('Confirm Password:')
    last_name = StringField('Last Name:', validators=[DataRequired()])
    first_name = StringField('First Name:', validators = [DataRequired()])
    middle_name = StringField('Middle Name:', validators=[Optional()])


class ForgotPasswordForm(FlaskForm):
    email = StringField('Enter your email:', validators=[DataRequired(), Email('Must be a valid email')], render_kw = {'autofocus': True, 'autocomplete': False})


class NewPasswordForm(FlaskForm):
    password = PasswordField('Enter New Password: ', validators=[DataRequired(), Length(min=8, max=255), EqualTo('confirm', message='password must match')], render_kw={ 'autofocus': True,})
    confirm = PasswordField('Confirm new Password: ')

class NewServiceForm(FlaskForm):
    title = StringField('Title: ', validators = [DataRequired()], render_kw ={'autofocus': True, 'autocomplete': False})
    details = StringField('Details: ', validators =[Optional(),], widget = TextArea())
    logo = FileField('Add logo: ', validators = [DataRequired(), FileAllowed(['jpg', 'png'], 'Image only!')], render_kw = {'required': True})
