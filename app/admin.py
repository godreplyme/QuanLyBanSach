from flask import redirect, url_for, request
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import current_user
from flask_sqlalchemy.track_modifications import models_committed
from wtforms.fields.simple import StringField
from flask_wtf import FlaskForm
from app import app, db
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from models import Sach, TheLoai, PhieuNhapSach, ChiTietNhapSach
from datetime import datetime


# Tùy chỉnh giao diện chính
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


# Tùy chỉnh giao diện cho Admin
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))



# Tùy chỉnh giao diện cho Nhân viên
class Importer(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_employee()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

    # Chỉ định các cột sử dụng trong form
    form_columns = ['id_Sach', 'soLuong']

    # Ghi đè các field mặc định
    form_overrides = {
        'id_Sach': QuerySelectField
    }

    # Cung cấp các query_factory cho các trường QuerySelectField
    form_args = {
        'id_Sach': {
            'query_factory': lambda: Sach.query.all(),
            'get_label': 'ten'
        }
    }

# Cấu hình Flask-Admin với template
admin = Admin(app=app, name='Quản lý hệ thống', template_mode='bootstrap4', index_view=MyAdminIndexView())

# Thêm bảng và quyền riêng
admin.add_view(AdminView(Sach, db.session, name='Quản lý Sách'))
admin.add_view(AdminView(TheLoai, db.session, name='Quản lý Thể Loại'))



# admin.add_view(PhieuNhapSachView(ChiTietNhapSach, db.session, name='Thêm Sách', endpoint='importbook'))
admin.add_view(Importer(ChiTietNhapSach,db.session, name="Phiếu", endpoint='importbook'))
