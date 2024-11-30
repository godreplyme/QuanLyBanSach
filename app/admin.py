from flask import redirect, url_for
from flask_login import current_user
from app import app, db
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from models import Sach, TheLoai, PhieuNhapSach


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
class ImporterView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_employee()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


# Cấu hình Flask-Admin với template
admin = Admin(app=app, name='Quản lý hệ thống', template_mode='bootstrap4', index_view=MyAdminIndexView())

# Thêm bảng và quyền riêng
admin.add_view(AdminView(Sach, db.session, name='Quản lý Sách'))
admin.add_view(AdminView(TheLoai, db.session, name='Quản lý Thể Loại'))
admin.add_view(ImporterView(PhieuNhapSach, db.session, name='Nhập Sách', endpoint='employee'))

