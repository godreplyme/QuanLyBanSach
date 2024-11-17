from sqlalchemy import Column, String, Integer, Boolean, Float, DateTime, ForeignKey, Date, column
from sqlalchemy.orm import relationship
from datetime import datetime,date
from app import db


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class VaiTro(BaseModel):
    __tablename__ = 'VaiTro'

    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class NguoiDung(BaseModel):
    __tablename__ = 'NguoiDung'

    username = Column(String(50), unique=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    hoVaTen = Column(String(50),default='')
    ngaySinh= Column(Date, default=date.today())
    gioiTinh= Column(Integer, default=0) # 0-nam 1-nu
    phone=Column(String(12), default='')
    email=Column(String(50),default='')
    address=Column(String(100),default='')
    avatar=Column(String(50),default='')# hoc den cloudinary roi sua default
    id_VaiTro= Column(Integer,ForeignKey(VaiTro.id))

class Sach(BaseModel):
    pass 

class TheLoai(BaseModel):
    pass
