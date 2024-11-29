from models import *
from __init__ import db, app
import os, hashlib


def get_book():
    return Sach.query.all()


def get_book_home():
    return Sach.query.filter(Sach.active.__eq__(True))


def get_category():
    return TheLoai.query.all()


def get_list_books(id_category=None, from_price=0, to_price=0):
    list_book = Sach.query.filter(Sach.active.__eq__(True))
    if id_category:
        list_book = list_book.filter(id_category == Sach.id_TheLoai)
    elif from_price:
        list_book = list_book.filter(from_price < Sach.donGia)
    elif to_price:
        list_book = list_book.filter(Sach.donGia < to_price)
    return list_book.all()


def add_user(name, username, password, **kw):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = NguoiDung(hoVaTen=name.strip()
                     ,username=username.strip()
                     ,password=password
                     ,anhDaiDien=kw.get('avatar')
                     ,email=kw.get('email'))
    with app.app_context():
        db.session.add(user)
        db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        return NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                                      NguoiDung.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)