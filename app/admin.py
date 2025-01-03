from flask import redirect, url_for, request
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_login import current_user, logout_user
from flask_sqlalchemy.track_modifications import models_committed
from wtforms.fields.simple import StringField
from __init__ import app, db
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from models import Sach, TheLoai, PhieuNhapSach, ChiTietNhapSach, NguoiDung, VaiTro, QuyDinh
from datetime import datetime
import dao


# def checkLoginAd():
#     if not current_user.is_authenticated:
#         return redirect("/login")


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        # check = checkLoginAd()
        # if check:
        #     return check

        stats = dao.count_book_by_cate()
        return self.render('admin/index.html', stats=stats)
    


# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_anonymous or current_user.vaiTro is VaiTro.ADMIN

#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('index'))


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.vaiTro is VaiTro.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class ProductView(AdminView):
    pass


class CategoryView(AdminView):
    can_export = True
    column_searchable_list = ['ten']
    column_filters = ['ten']
    can_view_details = True
    column_list = ['ten', 'sach']


class MyView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(MyView):
    @expose('/')
    def index(self):
        revenue_stats = dao.revenue_stats()
        frequency_stats = dao.frequency_stats()

        return self.render('admin/stats.html', revenue_stats=revenue_stats, frequency_stats=frequency_stats)


class ChangeView(AdminView):
    pass
    # @expose('/')
    # def index(self): 
        
    #     return self.render('admin/changeRules.html')


class LogoutView(MyView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect("/")


admin = Admin(app=app, name='Quản lý hệ thống', template_mode='bootstrap4', index_view=MyAdminIndexView())

admin.add_view(ProductView(Sach, db.session, name='Quản lý Sách'))
admin.add_view(CategoryView(TheLoai, db.session, name='Quản lý Thể Loại'))
admin.add_view(AdminView(NguoiDung, db.session, name='Quản lý Người Dùng'))
admin.add_view(StatsView(name='Thống Kê Báo Cáo'))
admin.add_view(ChangeView(QuyDinh, db.session, name='Thay đổi quy định'))
admin.add_view(LogoutView(name='Đăng xuất'))



