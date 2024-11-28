from models import *
from __init__ import db, app
import os


def get_book():
    return Sach.query.all()


def get_book_home():
    return Sach.query.filter(Sach.active.__eq__(True))


def get_category():
    return TheLoai.query.all()


def get_list_books( id_category=None, from_price=0, to_price=0):
    list_book = Sach.query.filter(Sach.active.__eq__(True))
    if id_category:
        list_book = list_book.filter(id_category == Sach.id_TheLoai)
    elif from_price:
        list_book = list_book.filter(from_price < Sach.donGia)
    elif to_price:
        list_book = list_book.filter(Sach.donGia < to_price)
    return list_book.all()

