from flask import flash, redirect, url_for

from app import app, db, utils
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from models import NguoiDung
from itsdangerous import URLSafeTimedSerializer


# Hàm tạo token (sử dụng itsdangerous để tạo token xác minh)
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Thay 'your_secret_key' bằng chuỗi bảo mật của bạn
    return serializer.dumps(email, salt='email-confirm-salt')


# Hàm xác minh token
def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Cùng secret key như khi tạo token
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except Exception:
        raise ValueError("Token xác minh không hợp lệ hoặc hết hạn.")
    return email
