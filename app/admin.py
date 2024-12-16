from flask import redirect, url_for, request
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import current_user
from flask_sqlalchemy.track_modifications import models_committed
from wtforms.fields.simple import StringField
from __init__ import app, db
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from models import Sach, TheLoai, PhieuNhapSach, ChiTietNhapSach
from datetime import datetime


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))




admin = Admin(app=app, name='Quản lý hệ thống', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(AdminView(Sach, db.session, name='Quản lý Sách'))
admin.add_view(AdminView(TheLoai, db.session, name='Quản lý Thể Loại'))



