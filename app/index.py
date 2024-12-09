import math, utils, cloudinary.uploader, admin, hashlib
from doctest import debug
from os import rename, renames
from models import *
from app import app, loginMNG, db
from flask import render_template, request, redirect, url_for, jsonify, flash




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


@app.route("/import", methods=['GET', 'POST'])
def import_book():
    list_import = utils.get_top_100_import()
    list_import_detail = []
    selected_import = None
    id_import = request.form.get('id_Import')
    if id_import:
        selected_import = utils.get_import_by_id(int(id_import))
        list_import_detail = db.session.query(ChiTietNhapSach.soLuong, Sach.ten.label("ten_sach"),
                                              Sach.tacGia.label("tac_gia"), TheLoai.ten.label("ten_the_loai")) \
            .join(Sach, ChiTietNhapSach.id_Sach == Sach.id) \
            .join(TheLoai, Sach.id_TheLoai == TheLoai.id) \
            .filter(ChiTietNhapSach.id_PhieuNhapSach == id_import) \
            .all()

    return render_template('importHome.html',
                           selected_import=selected_import,
                           list_import=list_import,
                           list_import_detail=list_import_detail)


@app.route('/importCreate', methods=['GET', 'POST'])
def create_import():
    if request.method == 'GET':
        keyword = request.args.get('q')
        if keyword:
            books = Sach.query.filter(Sach.ten.like(f"%{keyword}%")).all()
            results = [
                {
                    'id': book.id,
                    'ten': book.ten,
                    'tacGia': book.tacGia,
                    'theLoai': book.TheLoai.ten,
                    'soLuongTonKho': book.soLuongTonKho
                }
                for book in books
            ]
            return jsonify(results)
        return render_template('importCreate.html', today=datetime.now().strftime('%Y-%m-%d'))

    elif request.method == 'POST':
        data = request.json
        ngay_nhap = data.get('ngayNhap')
        sach_list = data.get('sachList', [])

        # Tạo phiếu nhập sách
        phieu_nhap = PhieuNhapSach(ngayNhapSach=ngay_nhap)
        db.session.add(phieu_nhap)

        # Lưu chi tiết nhập sách và cập nhật tồn kho
        for sach in sach_list:
            chi_tiet = ChiTietNhapSach(
                soLuong=sach['soLuong'],
                id_Sach=sach['id_Sach'],
                id_PhieuNhapSach=phieu_nhap.id
            )
            db.session.add(chi_tiet)

            # Cập nhật tồn kho
            sach_obj = Sach.query.get(sach['id_Sach'])
            sach_obj.soLuongTonKho += sach['soLuong']

        # Commit tất cả các thay đổi trong một lần
        db.session.commit()

        return jsonify({'success': True})


@app.route('/addBook', methods=['GET', 'POST'])
def add_book():
    err_msg=''
    suc_msg=''
    if request.method == 'POST':

        ten = request.form['ten']
        tacGia = request.form['tacGia']
        moTa = request.form.get('moTa', '')
        donGia = float(request.form['donGia'])
        id_TheLoai = int(request.form['id_TheLoai'])
        image = request.files['image']
        existing_book = Sach.query.filter_by(ten=ten, tacGia=tacGia).first()
        if existing_book:
            flash(f"Sách '{ten}' của tác giả '{tacGia}' đã tồn tại trong hệ thống.", 'danger')
            return redirect(url_for('add_book'))

        image_path = None
        if image:
            res = cloudinary.uploader.upload(image)
            image_path = res['secure_url']
        utils.add_book(ten=ten, tacGia=tacGia, donGia=donGia, moTa=moTa
                       ,id_TheLoai=id_TheLoai, image=image_path)
        flash('Đã thêm sách thành công.', 'success')
        return redirect(url_for('add_book'))
    theLoaiList = TheLoai.query.all()
    return render_template('addbook.html', theLoaiList=theLoaiList, err_msg=err_msg, suc_msg=suc_msg)


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
    app.run(debug=True)
