from models import *
from __init__ import db, app
import os


def load_book():
    return Sach.query.all()

def load_category():
    return TheLoai.query.all()