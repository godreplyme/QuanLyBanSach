from sqlalchemy import func
from models import *
from __init__ import db, app
import os, hashlib
import dao


def get_book():
    return Sach.query.all()


def get_book_home():
    return Sach.query.filter(Sach.active.__eq__(True))


def get_category():
    return TheLoai.query.all()


def get_list_books(id_category=None, from_price=0, to_price=0, kw=None):
    list_book = Sach.query.filter(Sach.active.__eq__(True))
    if id_category:
        list_book = list_book.filter(id_category == Sach.id_TheLoai)
    elif from_price:
        list_book = list_book.filter(from_price < Sach.donGia)
    elif to_price:
        list_book = list_book.filter(Sach.donGia < to_price)
    elif kw:
        list_book = list_book.filter(func.lower(Sach.ten).like(f"%{kw.lower()}%"))
    return list_book.all()


def add_user(name, username, password, **kw):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = NguoiDung(hoVaTen=name.strip()
                     , username=username.strip()
                     , password=password
                     , anhDaiDien=kw.get('avatar')
                     , email=kw.get('email'))
    with app.app_context():
        db.session.add(user)
        db.session.commit()


def check_login(username, password, role=None):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        u = NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                                      NguoiDung.password.__eq__(password))
        if role:
            u = u.filter(NguoiDung.vaiTro.__eq__(role))

        return u.first()


def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)


def get_book_by_id(book_id):
    return Sach.query.get(book_id)


def get_import():
    return PhieuNhapSach.query.order_by(PhieuNhapSach.ngayNhapSach.desc()).all()


def get_import_by_id(id=None):
    return PhieuNhapSach.query.get(id)

def add_book(ten, tacGia, donGia, **kw):
    sach = Sach(
        ten=ten,
        tacGia=tacGia,
        moTa=kw.get('moTa'),
        donGia=donGia,
        id_TheLoai=kw.get('id_TheLoai'),
        image=kw.get('image'),
    )
    with app.app_context():
        db.session.add(sach)
        db.session.commit()

def get_bill():
    return DonHang.query.order_by(DonHang.id.desc()).all()

def get_bill_by_id(id=None):
    return DonHang.query.get(id)

def get_qd():
    return QuyDinh.query.first()