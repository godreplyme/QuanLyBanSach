import math, utils, cloudinary.uploader, admin, hashlib
from os import rename, renames

from __init__ import app, loginMNG, db
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user


@app.context_processor
def default_response():
    return {
        'category': utils.get_category(),
        'sach': utils.get_book_home()
    }

@app.route("/")
def index():
    return render_template('home.html')


@app.route("/products")
def list_book():
    cate_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))
    kw = request.args.get('keyword')
    size = app.config['LIST_SIZE']
    start = (page - 1) * size
    end = start + size

    books = utils.get_list_books(id_category=cate_id, kw=kw)[start:end]
    l = len(utils.get_list_books(id_category=cate_id, kw=kw))
    return render_template('products.html',
                           page=math.ceil(l / app.config['LIST_SIZE']),
                           lb=books)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    err_msg = ''
    if request.method.__eq__('POST'):
        name = request.form.get('registerName')
        email = request.form.get('registerEmail')
        username = request.form.get('registerUserName')
        password = request.form.get('registerPassword')
        confirm = request.form.get('confirmPassword')
        avatar_path = None
        try:
            if password.__eq__(confirm):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']
                utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
                return redirect(url_for('login'))
            else:
                err_msg = 'Mật khẩu không khớp'

        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi: ' + str(ex)
    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = 'username hoặc password ko chính xác'
    return render_template('login.html', err_msg=err_msg)


@loginMNG.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    check = checkAuthenticated()
    if check:
        return check
    checkAuthenticated()
    return render_template('profile.html')


@app.route('/changeProfile', methods=['GET', 'POST'])
def changeProfile():
    check = checkAuthenticated()
    if check:
        return check
    if request.method.__eq__('POST'):
        checkAuthenticated()
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        email = request.form.get('email')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')

        current_user.hoVaTen = name
        current_user.sdt = phone
        current_user.diaChi = address
        current_user.email = email
        current_user.gioiTinh = 0 if gender == 'male' else 1
        current_user.ngaySinh = birthday
        try:
            db.session.commit()
            redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
    return render_template('changeProfile.html')


@app.route("/changePassword", methods=['GET', 'POST'])
def changePassword():
    err_msg = ''
    suc_msg = ''
    check = checkAuthenticated()
    if check:
        return check
    if request.method.__eq__('POST'):

        old = request.form.get('old')
        new = request.form.get('new')
        confirm = request.form.get('confirm')

        if current_user.password.__eq__(str(hashlib.md5(old.strip().encode('utf-8')).hexdigest())):
            if new.__eq__(confirm):
                current_user.password = str(hashlib.md5(new.strip().encode('utf-8')).hexdigest())
                db.session.commit()
                suc_msg = 'Đổi mật khẩu thành công'
            else:
                err_msg = 'Mật khẩu nhập lại không trùng khớp, mời nhập lại'
        else:
            err_msg = 'Mật khẩu cũ không đúng, mời nhập lại'
    return render_template('changePassword.html', err_msg=err_msg, suc_msg=suc_msg)


@app.route("/products/<int:sach_id>")
def productDetail(sach_id):
    book = utils.get_book_by_id(sach_id)
    return render_template('productDetail.html', sach=book)


@app.route("/import")
def import_book():
    return render_template('importHome.html')


@app.route('/importCreate')
def create_import():
    return render_template('importCreate.html')


@app.route('/addBook')
def add_book():
    return render_template('addBook.html')


def checkAuthenticated():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')


if __name__ == '__main__':
    app.run()
