from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from app import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class VaiTro(BaseModel):
    __tablename__ = 'VaiTro'

    name = Column(String(50), nullable=False, unique=True)

    nguoiDung = relationship('NguoiDung', backref='VaiTro', lazy=True)

    def __str__(self):
        return self.name


class NguoiDung(BaseModel):
    __tablename__ = 'NguoiDung'

    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    hoVaTen = Column(String(50), default='')
    ngaySinh = Column(Date, default=date.today())
    gioiTinh = Column(Integer, default=0)  # 0-nam 1-nu
    sdt = Column(String(12), default='')
    email = Column(String(50), default='')
    diaChi = Column(String(100), default='')
    anhDaiDien = Column(String(50), default='')  # hoc den cloudinary roi sua default
    vaiTro = Column(Integer, ForeignKey(VaiTro.id))

    donHang = relationship('DonHang', backref='NguoiDung', lazy=True)

    def __str__(self):
        return self.hoVaTen


class Sach(BaseModel):
    __tablename__ = 'Sach'

    ten = Column(String(100), nullable=False)
    tacGia = Column(String(50), nullable=False)
    moTa = Column(String(255), default='')
    donGia = Column(Float, nullable=False, default=0)
    soLuongTonKho = Column(Integer, nullable=False, default=0)
    id_TheLoai = Column(Integer, ForeignKey('TheLoai.id'))

    chiTietDonHang = relationship('ChiTietDonHang', backref='Sach', lazy=True)
    chiTietNhapSach = relationship('ChiTietNhapSach', backref='Sach', lazy=True)
    def __str__(self):
        return self.ten


class TheLoai(BaseModel):
    __tablename__ = 'TheLoai'

    ten = Column(String(100), nullable=False)

    sach = relationship('Sach', backref='TheLoai', lazy=True)

    def __str__(self):
        return self.ten


class DonHang(BaseModel):
    __tablename__ = 'DonHang'

    ngayDatHang = Column(DateTime, default=datetime.now())
    ngayThanhToan = Column(DateTime)
    tongTien = Column(Float)

    trangThai = Column(Integer, ForeignKey('TrangThai.id'))
    phuongThucThanhToan = Column(Integer, ForeignKey('PhuongThucThanhToan.id'))
    nguoiDung = Column(Integer, ForeignKey(NguoiDung.id))
    chiTietDonHang = relationship('ChiTietDonHang', backref='DonHang', lazy=True)

    def __str__(self):
        return self.__tablename__ + self.id


class TrangThai(BaseModel):
    __tablename__ = 'TrangThai'

    ten = Column(String(50), nullable=False)

    donHang = relationship('DonHang', backref='TrangThai', lazy=True)

    def __str__(self):
        return self.ten


class PhuongThucThanhToan(BaseModel):
    __tablename__ = 'PhuongThucThanhToan'

    ten = Column(String(50), nullable=False)

    donHang = relationship('DonHang', backref='PhuongThucThanhToan', lazy=True)

    def __str__(self):
        return self.ten


class ChiTietDonHang(BaseModel):
    __tablename__ = 'ChiTietDonHang'

    id_Sach = Column(Integer, ForeignKey(Sach.id))
    id_DonHang = Column(Integer, ForeignKey(DonHang.id))
    soLuong = Column(Integer, nullable=False)
    tongTien = Column(Float, nullable=False)

    def __str__(self):
        return self.__tablename__ + self.id_Sach + self.id_DonHang


class PhieuNhapSach(BaseModel):
    __tablename__ = 'PhieuNhapSach'

    ngayNhapSach = Column(DateTime, nullable=False, default=datetime.now())

    chiTietNhapSach = relationship('ChiTietNhapSach', backref='PhieuNhapSach', lazy=True)

    def __str__(self):
        return self.__tablename__ + self.id


class ChiTietNhapSach(BaseModel):
    __tablename__ = 'ChiTietNhapSach'

    soLuong = Column(Integer, nullable=False)
    id_Sach = Column(Integer, ForeignKey(Sach.id))
    id_PhieuNhapSach = Column(Integer, ForeignKey(PhieuNhapSach.id))

    def __str__(self):
        return self.__tablename__ + self.id

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
