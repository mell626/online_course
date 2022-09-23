from .imports import *
from .models import *
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView



class UserView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return True

    can_delete = False
    can_create = True
    column_exclude_list =['password_hash',]

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('default'))


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('default'))


class ExtensionServiceView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return True

    can_delete = False
    can_create = True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('default'))

class CourseView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return True
        return True

    can_delete = False
    can_create = True
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('default'))


admin = Admin(index_view = MyAdminIndexView())

admin.add_view(UserView(User, db.session))
admin.add_view(ExtensionServiceView(ExtensionService, db.session))
admin.add_view(CourseView(Course, db.session))