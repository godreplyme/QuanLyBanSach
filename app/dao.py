from flask_login import current_user
from models import Sach, NguoiDung, VaiTro, TrangThai, TheLoai, DonHang, ChiTietDonHang 
from __init__ import app, db
import utils
import hashlib
import cloudinary.uploader

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
