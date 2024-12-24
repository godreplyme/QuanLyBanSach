from flask_login import current_user
from models import Sach, NguoiDung, VaiTro, TrangThai, TheLoai, DonHang, ChiTietDonHang 
from __init__ import app, db
import utils
import hashlib
import cloudinary.uploader
from sqlalchemy import func
from datetime import datetime

def save_order(cart):
    if cart: # cart khac null
        order = DonHang(NguoiDung=current_user) # backref
        db.session.add(order)

        for c in cart.values(): 
            if Sach.soLuongTonKho >= c['soLuong']:
                detail = ChiTietDonHang(soLuong=c['soLuong'], tongTien=c['tongTien'],
                                        DonHang=order, id_Sach=c['id'])
                Sach.soLuongTonKho -= c['soLuong']
            else:
                raise ValueError("{} số lượng tồn không đủ".format(Sach.ten))
            db.session.add(detail)
        db.session.commit()


def count_books():
    return Sach.query.count()


def count_book_by_cate():
    return db.session.query(TheLoai.id, TheLoai.ten, func.count(Sach.id))\
             .join(Sach, Sach.id_TheLoai.__eq__(TheLoai.id), isouter=True)\
             .group_by(TheLoai.id).all()


def revenue_stats(kw=None):
    query = db.session.query(Sach.id, Sach.ten, func.sum(ChiTietDonHang.soLuong * ChiTietDonHang.tongTien))\
                      .join(ChiTietDonHang, ChiTietDonHang.id_Sach.__eq__(Sach.id)).group_by(Sach.id)

    if kw:
        query = query.filter(Sach.ten.contains(kw))

    return query.all()


def frequency_stats(p='month', year=datetime.now().year):
    return db.session.query(func.extract(p, DonHang.ngayThanhToan),
                            func.sum(ChiTietDonHang.soLuong * ChiTietDonHang.tongTien))\
                      .join(ChiTietDonHang, ChiTietDonHang.id_DonHang.__eq__(DonHang.id))\
                      .group_by(func.extract(p, DonHang.ngayThanhToan), func.extract('year', DonHang.ngayThanhToan))\
                      .filter(func.extract('year', DonHang.ngayThanhToan).__eq__(year)).all()


if __name__ == '__main__':
    with app.app_context():
        print(revenue_stats())