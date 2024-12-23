from flask_login import current_user
from sqlalchemy import func
from models import *
from __init__ import db, app
import os, hashlib
import dao


def get_book():
    return Sach.query.all()


def get_book_home():
    return Sach.query.filter(Sach.active.__eq__(True)).limit(15).all()


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
def get_user_by_username(username=None):
    return NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip())).first()


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


def add_comment(noiDung=None, sach_id=None):
    c = BinhLuan(noiDung=noiDung, id_Sach=sach_id, NguoiDung=current_user)
    db.session.add(c)
    db.session.commit()

    return c


def get_book_pagination(category_id=None, page=1, kw=None):
    sach = Sach.query
    if kw:
        sach = sach.filter(Sach.ten.contain(kw))
    if category_id:
        sach = sach.filter(Sach.id_TheLoai == category_id)
    page_size = app.config['LIST_SIZE']
    start = (page - 1) * page_size

    return sach.slice(start, start + page_size).all()


def count_book(category_id=None, kw=None):
    sach = Sach.query
    if kw:
        sach = sach.filter(Sach.ten.contain(kw))
    if category_id:
        sach = sach.filter(Sach.id_TheLoai == category_id)

    return sach.count()


def get_commment(sach_id=None, page=1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size

    return BinhLuan.query.filter(Sach.id == sach_id).order_by(-BinhLuan.id).slice(start, start + page_size).all()


def count_comment(sach_id):
    return BinhLuan.query.filter(BinhLuan.id_Sach == sach_id).count()

def get_user_by_email(email):
    return NguoiDung.query.filter(NguoiDung.email.__eq__(email)).first()

def get_bill_pagination(page=1):
    page_size = app.config['LIST_SIZE']
    start = (page - 1) * page_size
    return db.session.query(DonHang.id.label('id_don_hang'),
                     DonHang.ngayDatHang.label('ngay_dat_hang'),
                     DonHang.phuongThucThanhToan.label('pttt'),
                     NguoiDung.hoVaTen.label('ten_user'),
                     DonHang.trangThai.label('trang_thai'),
                     func.sum(Sach.donGia * ChiTietDonHang.soLuong).label('tong_gia')) \
        .select_from(DonHang).join(ChiTietDonHang, DonHang.id == ChiTietDonHang.id_DonHang) \
        .join(Sach, ChiTietDonHang.id_Sach == Sach.id) \
        .join(NguoiDung, DonHang.nguoiDung == NguoiDung.id) \
        .group_by(DonHang.id, DonHang.ngayDatHang, DonHang.phuongThucThanhToan, NguoiDung.hoVaTen,
                  DonHang.trangThai).order_by(DonHang.id.desc()).slice(start, start + page_size).all()

def count_bill_pagination():
    return db.session.query(DonHang.id.label('id_don_hang'),
                     DonHang.ngayDatHang.label('ngay_dat_hang'),
                     DonHang.phuongThucThanhToan.label('pttt'),
                     NguoiDung.hoVaTen.label('ten_user'),
                     DonHang.trangThai.label('trang_thai'),
                     func.sum(Sach.donGia * ChiTietDonHang.soLuong).label('tong_gia')) \
        .select_from(DonHang).join(ChiTietDonHang, DonHang.id == ChiTietDonHang.id_DonHang) \
        .join(Sach, ChiTietDonHang.id_Sach == Sach.id) \
        .join(NguoiDung, DonHang.nguoiDung == NguoiDung.id) \
        .group_by(DonHang.id, DonHang.ngayDatHang, DonHang.phuongThucThanhToan, NguoiDung.hoVaTen,
                  DonHang.trangThai).count()

def count_bill():
    return DonHangOffline.query.count()

def get_order():
    if not current_user.is_authenticated:
        return []

    return db.session.query(
        DonHang.id.label('id_don_hang'),
        DonHang.ngayDatHang.label('ngay_dat_hang'),
        DonHang.trangThai.cast(Integer).label('trang_thai'),
        ChiTietDonHang.soLuong.label('so_luong'),
        Sach.donGia.label('don_gia'),
        Sach.ten.label('ten_sach'),
        Sach.image.label('image'),
        NguoiDung.id.label('id_nguoi_dung')
    ).select_from(DonHang)\
        .join(ChiTietDonHang, DonHang.id == ChiTietDonHang.id_DonHang)\
        .join(Sach, Sach.id == ChiTietDonHang.id_Sach)\
        .join(NguoiDung, NguoiDung.id == DonHang.nguoiDung)\
        .filter(current_user.id == DonHang.nguoiDung)\
        .order_by(DonHang.ngayDatHang.desc())\
        .all()