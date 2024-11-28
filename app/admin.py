from app import app, db
from flask_admin import Admin
from models import Sach, TheLoai
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name='Người quản trị', template_mode='bootstrap4')

admin.add_view(ModelView(Sach, db.session))
admin.add_view(ModelView(TheLoai, db.session))
