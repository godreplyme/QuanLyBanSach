import hashlib
from logging.config import valid_ident
from sqlalchemy import Column, String, Integer, Boolean, Date, Float, Enum as SQLEnum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import date, datetime
from __init__ import db, app
from enum import Enum
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Boolean, Date, Float, Enum as SQLEnum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship

from __init__ import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class VaiTro(Enum):
    ADMIN = 1
    USER = 2
    EMPLOYEE = 3
    IMPORTER = 4

    def __str__(self):
        if self == VaiTro.ADMIN:
            return 'Người quản trị'
        elif self == VaiTro.USER:
            return 'Khách hàng'
        elif self == VaiTro.EMPLOYEE:
            return 'Nhân viên bán sách'
        elif self == VaiTro.IMPORTER:
            return 'Nhân viên nhập sách'

class TrangThai(Enum):
    DA_DAT_HANG = 1
    DANG_CHO_THANH_TOAN = 2
    DANG_GIAO_HANG = 3
    DA_NHAN_HANG = 4
    CHO_NHAN_HANG = 5
    DA_HUY = 6

    def __str__(self):
        if self == TrangThai.DA_DAT_HANG:
            return 'Đã đặt hàng'
        elif self == TrangThai.DANG_CHO_THANH_TOAN:
            return 'Đang chờ thanh toán'
        elif self == TrangThai.DANG_GIAO_HANG:
            return 'Đang giao hàng'
        elif self == TrangThai.DA_NHAN_HANG:
            return 'Đã nhận hàng'
        elif self == TrangThai.CHO_NHAN_HANG:
            return 'Chờ nhận hàng'
        elif self == TrangThai.DA_HUY:
            return 'Đã hủy'


class PhuongThucThanhToan(Enum):
    TRUC_TIEP = 1
    TRUC_TUYEN = 2

    def __str__(self):
        return "Trực tiếp" if self == PhuongThucThanhToan.TRUC_TIEP else "Trực tuyến"


# Cơ sở dữ liệu cho người dùng
class NguoiDung(BaseModel,UserMixin):
    __tablename__ = 'NguoiDung'
    __table_args__ = {'extend_existing': True}

    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False, default='')
    active = Column(Boolean, default=True)
    hoVaTen = Column(String(50), nullable=False, default='')
    ngaySinh = Column(Date, default=date.today())
    gioiTinh = Column(Integer, default=0)  # 0-nam 1-nu
    sdt = Column(String(12), default='')
    email = Column(String(50), default='')
    diaChi = Column(String(100), default='')
    anhDaiDien = Column(String(255), default='')  # Đường dẫn ảnh đại diện
    vaiTro = Column(SQLEnum(VaiTro), default=VaiTro.USER)

    phieuNhapSach = relationship('PhieuNhapSach', backref='NguoiDung', lazy=True)
    donHang = relationship('DonHang', backref='NguoiDung', lazy=True)
    gioHang = relationship('GioHang', backref='NguoiDung', lazy=True)

    def is_admin(self):
        return self.vaiTro == VaiTro.ADMIN

    def is_employee(self):
        return self.vaiTro == VaiTro.EMPLOYEE

    def is_importer(self):
        return self.vaiTro == VaiTro.IMPORTER

    def __str__(self):
        return self.hoVaTen


class Sach(BaseModel):
    __tablename__ = 'Sach'

    ten = Column(String(100), nullable=False)
    tacGia = Column(String(50), nullable=False)
    moTa = Column(Text, default='')
    donGia = Column(Float, nullable=False, default=0)
    soLuongTonKho = Column(Integer, nullable=False, default=0)
    id_TheLoai = Column(Integer, ForeignKey('TheLoai.id'))
    image = Column(String(255))
    active = Column(Boolean, nullable=False, default=True)

    chiTietDonHang = relationship('ChiTietDonHang', backref='Sach', lazy=True)
    chiTietNhapSach = relationship('ChiTietNhapSach', backref='Sach', lazy=True)
    chiTietGioHang = relationship('ChiTietGioHang', backref='Sach', lazy=True)

    def __str__(self):
        return self.ten


class GioHang(BaseModel):
    __tablename__ = 'GioHang'

    nguoiDung = Column(Integer, ForeignKey(NguoiDung.id))
    chiTietGioHang = relationship('ChiTietGioHang', backref='GioHang', lazy=True)


class ChiTietGioHang(BaseModel):
    __tablename__ = 'ChiTietGioHang'

    soLuong = Column(Integer, nullable=False, default=1)
    gioHang = Column(Integer, ForeignKey(GioHang.id))
    sach = Column(Integer, ForeignKey(Sach.id))


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

    trangThai = Column(SQLEnum(TrangThai), default=TrangThai.DA_DAT_HANG, nullable=False)
    phuongThucThanhToan = Column(SQLEnum(PhuongThucThanhToan), nullable=False)
    nguoiDung = Column(Integer, ForeignKey(NguoiDung.id), nullable=True)
    chiTietDonHang = relationship('ChiTietDonHang', backref='DonHang', lazy=True)

    def __str__(self):
        return self.__tablename__ + self.id


class ChiTietDonHang(BaseModel):
    __tablename__ = 'ChiTietDonHang'

    id_Sach = Column(Integer, ForeignKey(Sach.id))
    id_DonHang = Column(Integer, ForeignKey(DonHang.id))
    soLuong = Column(Integer, nullable=False)

    def __str__(self):
        return self.__tablename__ + self.id_Sach + self.id_DonHang


class PhieuNhapSach(BaseModel):
    __tablename__ = 'PhieuNhapSach'

    id_NguoiDung = Column(Integer, ForeignKey(NguoiDung.id))
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


class QuyDinh(BaseModel):
    __tablename__ = 'QuyDinh'

    soLuongNhapToiThieu = Column(Integer, nullable=False, default=150)
    gioiHanNhap = Column(Integer, nullable=False, default=300)
    thoiGianQuyDinh = Column(Integer, nullable=False, default=48)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        cat = [
            TheLoai(ten='Tiểu thuyết'),
            TheLoai(ten='Truyện ngắn'),
            TheLoai(ten='Ngôn tình'),
            TheLoai(ten='Truyện Tranh'),
            TheLoai(ten='Trinh thám'),
            TheLoai(ten='Sách giáo khoa'),
            TheLoai(ten='Marketing'),
            TheLoai(ten='Phân tích kinh tế'),
            TheLoai(ten='Light novel'),
            TheLoai(ten='Tô màu, luyện chữ'),
            TheLoai(ten='Sách kiến thức- kĩ năng sống cho trẻ'),
            TheLoai(ten='Văn học')
        ]
        db.session.add_all(cat)
        db.session.commit()
        sach = [Sach(ten="Chí Phèo", tacGia="Nam Cao",
                     moTa="Tác phẩm kinh điển của văn học Việt Nam, kể về bi kịch của Chí Phèo.", donGia=75000,
                     soLuongTonKho=50, id_TheLoai=12,
                     image="https://cdn0.fahasa.com/media/catalog/product/i/m/image_193731.jpg"),
                Sach(ten="Đắc Nhân Tâm", tacGia="Dale Carnegie",
                     moTa="Cuốn sách dạy cách giao tiếp và tạo ảnh hưởng lớn nhất mọi thời đại.", donGia=95000,
                     soLuongTonKho=30, id_TheLoai=11,
                     image="https://cdn0.fahasa.com/media/catalog/product/9/7/9786043949247.jpg"),
                Sach(ten="Dế Mèn Phiêu Lưu Ký", tacGia="Tô Hoài",
                     moTa="Cuốn sách gắn liền với tuổi thơ của nhiều thế hệ.", donGia=50000, soLuongTonKho=100,
                     id_TheLoai=12, image="https://cdn0.fahasa.com/media/catalog/product/d/e/de-men-50k_1.jpg"),
                Sach(ten="Vũ Trụ Trong Vỏ Hạt Dẻ", tacGia="Stephen Hawking",
                     moTa="Một trong những cuốn sách khoa học nổi tiếng nhất của Stephen Hawking.", donGia=120000,
                     soLuongTonKho=20, id_TheLoai=1,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8934974179597.jpg"),
                Sach(ten="English Grammar in Use", tacGia="Raymond Murphy",
                     moTa="Cuốn sách ngữ pháp tiếng Anh được hàng triệu người học sử dụng.", donGia=150000,
                     soLuongTonKho=15, id_TheLoai=2,
                     image="https://cdn0.fahasa.com/media/catalog/product/9/7/9781108430425.jpg"),
                Sach(ten="Tôi Thấy Hoa Vàng Trên Cỏ Xanh", tacGia="Nguyễn Nhật Ánh",
                     moTa="Một câu chuyện tuổi thơ đầy cảm xúc và ký ức đẹp.", donGia=72.50,
                     soLuongTonKho=25, id_TheLoai=1,
                     image="https://cdn0.fahasa.com/media/catalog/product/n/n/nna-hvtcx.jpg"),
                Sach(ten="Nhà Giả Kim", tacGia="Paulo Coelho",
                     moTa="Một hành trình tìm kiếm ước mơ và khám phá bản thân.", donGia=100.00,
                     soLuongTonKho=12, id_TheLoai=3,
                     image="https://cdn0.fahasa.com/media/catalog/product/i/m/image_195509_1_36793.jpg"),
                Sach(ten="Mắt Biếc", tacGia="Nguyễn Nhật Ánh",
                     moTa="Một chuyện tình đầy day dứt và thơ mộng.", donGia=65.00,
                     soLuongTonKho=18, id_TheLoai=1,
                     image="https://cdn0.fahasa.com/media/catalog/product/n/x/nxbtre_full_06402022_014041.jpg"),
                Sach(ten="Chuyện Người Con Gái Nam Xương", tacGia="Nguyễn Dữ",
                     moTa="Một tác phẩm kinh điển của văn học Việt Nam thời xưa.", donGia=50.00,
                     soLuongTonKho=40, id_TheLoai=4,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8932000130116_thanh_ly.jpg"),
                Sach(ten="Tắt Đèn", tacGia="Ngô Tất Tố",
                     moTa="Tác phẩm miêu tả cuộc sống cơ cực của người nông dân Việt Nam.", donGia=60.00,
                     soLuongTonKho=15, id_TheLoai=6,
                     image="https://cdn0.fahasa.com/media/catalog/product/9/7/9786043947441.jpg"),
                Sach(ten="Hạt Giống Tâm Hồn", tacGia="Nhiều Tác Giả",
                     moTa="Tuyển tập những câu chuyện truyền cảm hứng và ý nghĩa.", donGia=70.00,
                     soLuongTonKho=22, id_TheLoai=2,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8935086857434.jpg"),
                Sach(ten="Sống Mòn", tacGia="Nam Cao",
                     moTa="Một câu chuyện sâu sắc về cuộc sống và thân phận con người.", donGia=58.00,
                     soLuongTonKho=28, id_TheLoai=4,
                     image="https://cdn0.fahasa.com/media/catalog/product/9/7/9786044916927.jpg"),
                Sach(ten="Lão Hạc", tacGia="Nam Cao",
                     moTa="Tác phẩm xúc động về cuộc đời một lão nông nghèo khổ.", donGia=52.00,
                     soLuongTonKho=24, id_TheLoai=4,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8935236427838.jpg"),
                Sach(ten="Những Người Khốn Khổ", tacGia="Victor Hugo",
                     moTa="Câu chuyện kinh điển về lòng nhân ái và sự hi sinh.", donGia=120.00,
                     soLuongTonKho=10, id_TheLoai=7,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8935086840252.jpg"),
                Sach(ten="Bến Không Chồng", tacGia="Dương Hướng",
                     moTa="Tác phẩm cảm động về cuộc sống vùng quê Việt Nam sau chiến tranh.", donGia=65.00,
                     soLuongTonKho=16, id_TheLoai=5,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8934974180272.jpg"),
                Sach(ten="Chiếc Lá Cuối Cùng", tacGia="O. Henry",
                     moTa="Câu chuyện về lòng hy sinh và tình yêu thương trong cuộc sống.", donGia=45.00,
                     soLuongTonKho=25, id_TheLoai=8,
                     image="https://cdn0.fahasa.com/media/catalog/product/8/9/8936067605051.jpg"),
                Sach(ten="Quân Khu Nam Đồng", tacGia="Bình Ca",
                     moTa="Những hồi ức đẹp đẽ về một thời tuổi trẻ rực rỡ.", donGia=75.00,
                     soLuongTonKho=18, id_TheLoai=9,
                     image="https://cdn0.fahasa.com/media/catalog/product/n/x/nxbtre_full_21352023_023516_1.jpg")
                ]
        db.session.add_all(sach)
        db.session.commit()
        admin = NguoiDung(hoVaTen='Hồ Vũ', username='admin'
                          , password='698d51a19d8a121ce581499d7b701668'  # username: admin, pass: 111
                          , email='vu123@gmail.com', vaiTro=VaiTro.ADMIN
                          ,anhDaiDien='https://res.cloudinary.com/dcrsia5sh/image/upload/v1732855504/mpkxldxtz440munykvf5.jpg')
        customer = NguoiDung(hoVaTen='Vũ', username='user'
                             , password='698d51a19d8a121ce581499d7b701668'  # username: user, pass: 111
                             , email='vu123@gmail.com', vaiTro=VaiTro.USER
                             ,anhDaiDien='https://res.cloudinary.com/dcrsia5sh/image/upload/v1732855504/mpkxldxtz440munykvf5.jpg')
        employee = NguoiDung(hoVaTen='Nguyễn Vũ', username='employee'
                             , password='698d51a19d8a121ce581499d7b701668'  # username: employee, pass: 111
                             , email='vu123@gmail.com', vaiTro=VaiTro.EMPLOYEE
                             ,anhDaiDien='https://res.cloudinary.com/dcrsia5sh/image/upload/v1732855504/mpkxldxtz440munykvf5.jpg')
        importer = NguoiDung(hoVaTen='Nguyễn Vũ', username='importer'
                             , password='698d51a19d8a121ce581499d7b701668'  # username: importer, pass: 111
                             , email='vu123@gmail.com', vaiTro=VaiTro.IMPORTER
                             ,anhDaiDien='https://res.cloudinary.com/dcrsia5sh/image/upload/v1732855504/mpkxldxtz440munykvf5.jpg')
        db.session.add_all([admin, customer, employee, importer])

        phieuNhapSach = [
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 1), id_NguoiDung=4),
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 2), id_NguoiDung=4),
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 3), id_NguoiDung=4),
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 4), id_NguoiDung=4),
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 5), id_NguoiDung=4),
            PhieuNhapSach(ngayNhapSach=datetime(2024, 12, 6), id_NguoiDung=4    )
        ]
        chiTietNhapSach = [
            ChiTietNhapSach(soLuong=50, id_Sach=1, id_PhieuNhapSach=1),
            ChiTietNhapSach(soLuong=20, id_Sach=2, id_PhieuNhapSach=1),
            ChiTietNhapSach(soLuong=30, id_Sach=3, id_PhieuNhapSach=2),
            ChiTietNhapSach(soLuong=40, id_Sach=4, id_PhieuNhapSach=2)
        ]
        db.session.add_all(phieuNhapSach)
        db.session.add_all(chiTietNhapSach)

        don_hang = [
            DonHang(ngayDatHang=datetime(2024, 12, 1), ngayThanhToan=datetime(2024, 12, 11),
                    trangThai=TrangThai.DA_DAT_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP, nguoiDung=1),
            DonHang(ngayDatHang=datetime(2024, 12, 2), ngayThanhToan=datetime(2024, 12, 12),
                    trangThai=TrangThai.DANG_CHO_THANH_TOAN, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TUYEN,
                    nguoiDung=2),
            DonHang(ngayDatHang=datetime(2024, 12, 3), ngayThanhToan=datetime(2024, 12, 13),
                    trangThai=TrangThai.DANG_GIAO_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP, nguoiDung=3),
            DonHang(ngayDatHang=datetime(2024, 12, 4), ngayThanhToan=datetime(2024, 12, 14),
                    trangThai=TrangThai.DA_NHAN_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TUYEN, nguoiDung=1),
            DonHang(ngayDatHang=datetime(2024, 12, 5), ngayThanhToan=datetime(2024, 12, 15), trangThai=TrangThai.DA_HUY,
                    phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP, nguoiDung=2),
            DonHang(ngayDatHang=datetime(2024, 12, 6), ngayThanhToan=datetime(2024, 12, 16),
                    trangThai=TrangThai.DA_DAT_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TUYEN, nguoiDung=3),
            DonHang(ngayDatHang=datetime(2024, 12, 7), ngayThanhToan=datetime(2024, 12, 17),
                    trangThai=TrangThai.DANG_CHO_THANH_TOAN, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP,
                    nguoiDung=1),
            DonHang(ngayDatHang=datetime(2024, 12, 8), ngayThanhToan=datetime(2024, 12, 18),
                    trangThai=TrangThai.DANG_GIAO_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TUYEN,
                    nguoiDung=2),
            DonHang(ngayDatHang=datetime(2024, 12, 9), ngayThanhToan=datetime(2024, 12, 19),
                    trangThai=TrangThai.DA_NHAN_HANG, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP, nguoiDung=3),
            DonHang(ngayDatHang=datetime(2024, 12, 10), ngayThanhToan=datetime(2024, 12, 20),
                    trangThai=TrangThai.DA_HUY, phuongThucThanhToan=PhuongThucThanhToan.TRUC_TUYEN, nguoiDung=1)
        ]
        db.session.add_all(don_hang)
        chi_tiet_don_hang = [
            ChiTietDonHang(id_Sach=1, id_DonHang=1, soLuong=2),
            ChiTietDonHang(id_Sach=2, id_DonHang=1, soLuong=3),
            ChiTietDonHang(id_Sach=3, id_DonHang=2, soLuong=1),
            ChiTietDonHang(id_Sach=4, id_DonHang=2, soLuong=5),
            ChiTietDonHang(id_Sach=5, id_DonHang=3, soLuong=2),
            ChiTietDonHang(id_Sach=6, id_DonHang=3, soLuong=1),
            ChiTietDonHang(id_Sach=7, id_DonHang=4, soLuong=4),
            ChiTietDonHang(id_Sach=8, id_DonHang=4, soLuong=2),
            ChiTietDonHang(id_Sach=9, id_DonHang=5, soLuong=1),
            ChiTietDonHang(id_Sach=10, id_DonHang=5, soLuong=3),
            ChiTietDonHang(id_Sach=11, id_DonHang=6, soLuong=2),
            ChiTietDonHang(id_Sach=12, id_DonHang=6, soLuong=1),
            ChiTietDonHang(id_Sach=13, id_DonHang=7, soLuong=5),
            ChiTietDonHang(id_Sach=14, id_DonHang=7, soLuong=2),
            ChiTietDonHang(id_Sach=15, id_DonHang=8, soLuong=4),
            ChiTietDonHang(id_Sach=16, id_DonHang=8, soLuong=1),
            ChiTietDonHang(id_Sach=1, id_DonHang=9, soLuong=2),
            ChiTietDonHang(id_Sach=2, id_DonHang=9, soLuong=3),
            ChiTietDonHang(id_Sach=3, id_DonHang=10, soLuong=4),
            ChiTietDonHang(id_Sach=4, id_DonHang=10, soLuong=2)
        ]
        db.session.add_all(chi_tiet_don_hang)
        quy_dinh=QuyDinh(soLuongNhapToiThieu=150, gioiHanNhap=300, thoiGianQuyDinh=48)
        db.session.add(quy_dinh)
        gio_hang=[
            GioHang(nguoiDung=1),GioHang(nguoiDung=2),GioHang(nguoiDung=3)
        ]
        db.session.add_all(gio_hang)
        db.session.commit()
