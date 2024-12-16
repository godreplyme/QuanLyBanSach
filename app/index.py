import math, utils, cloudinary.uploader, admin, hashlib
from os import rename, renames

from __init__ import app, loginMNG, db
from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import ChiTietDonHang, DonHang, NguoiDung, TrangThai, GioHang, ChiTietGioHang, Sach

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


@app.route('/products/<int:sach_id>')
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
    if not current_user.is_authenticated:
        return redirect('/login')
    # Giả sử bạn lấy đơn hàng từ database dựa trên user_id
    current_user_id = current_user.id # ID người dùng hiện tại (nếu có đăng nhập)

    #lấy giỏ hàng của người dùng đang đăng nhập hiện tại ( mỗi người chỉ có 1 giỏ hàng)
    gio_hang = GioHang.query.filter_by(nguoiDung=current_user_id).first()
    if not gio_hang:
        return render_template('cart.html', carts=[]) # nếu giỏ hàng rỗng thì trả về rỗng
    #lấy danh sách chi tiết giỏ hàng của người dùng
    chi_tiet_GH = ChiTietGioHang.query.filter_by(gioHang=gio_hang.id).all()

    danh_sach_sach = []
    for chi_tiet in chi_tiet_GH:
        danh_sach_sach.append({
            'image': chi_tiet.sach.image,
            'ten': chi_tiet.sach.ten,
            'tacGia': chi_tiet.sach.tacGia,
            'soLuong': chi_tiet.soLuong,
            'donGia': chi_tiet.sach.donGia,
            'tongTien': chi_tiet.soLuong * chi_tiet.sach.donGia,  # Tính tổng tiền
        })
    # Truyền dữ liệu vào template giỏ hàng
    return render_template('cart.html', carts=danh_sach_sach)

# # Lấy đơn hàng ở trạng thái TRONG_GIO_HANG
    # don_hangs = DonHang.query.filter_by(nguoiDung=current_user_id, trangThai=TrangThai.TRONG_GIO_HANG).all()
    # # Lấy danh sách sách thông qua ChiTietDonHang
    # danh_sach_sach=[]
    # for don_hang in don_hangs:
    #    chi_tiet_DH = ChiTietDonHang.query.filter_by(id_DonHang=don_hang.id).all()
    #    for chi_tiet in chi_tiet_DH:
    #        danh_sach_sach.append({
    #            'image':chi_tiet.sach.image,
    #            'ten': chi_tiet.sach.ten,
    #            'tacGia': chi_tiet.sach.tacGia,
    #            'soLuong': chi_tiet.soLuong,
    #            'donGia': chi_tiet.sach.donGia,
    #            'tongTien': chi_tiet.tongTien,
    #        })
    # print("Danh sách đơn hàng:", don_hangs)
    # for don_hang in don_hangs:
    #     chi_tiet_DH = ChiTietDonHang.query.filter_by(id_DonHang=don_hang.id).all()
    #     print("Chi tiết đơn hàng:", chi_tiet_DH)
    # print("Danh sách sách:", danh_sach_sach)
    # # Chuyển dữ liệu đơn hàng vào template
    # return render_template('cart.html', carts=danh_sach_sach)


@app.route('/products/<int:sach_id>', methods=['POST'])
@login_required
def add_to_cart(sach_id):
    # Lấy số lượng từ body của yêu cầu
    print(request)
    if request.method=='POST':
        data = request.get_json()  # Lấy dữ liệu JSON từ body của POST request
        print(data)
        quantity = data.get('quantity')  # Lấy giá trị số lượng, mặc định là 1 nếu không có
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        # Lấy giỏ hàng của người dùng
        gio_hang = GioHang.query.filter_by(nguoiDung=current_user.id).first()
        # #truy vấn sản phẩm theo id
        # product = Sach.query.filter_by(id=sach_id).first()
        if gio_hang is None:
            # Nếu không có giỏ hàng, tạo mới giỏ hàng cho người dùng
            gio_hang = GioHang(nguoiDung=current_user.id)
            db.session.add(gio_hang)
            db.session.commit()
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        chi_tiet = ChiTietGioHang.query.filter(
            ChiTietGioHang.gioHang == gio_hang.id,  # Đảm bảo `gio_hang` là một đối tượng
            ChiTietGioHang.sachID == sach_id).first()  # Đảm bảo `sach` là một đối tượng

        if chi_tiet:
            # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng lên
            chi_tiet.soLuong += int(quantity)
        else:
            # Nếu sản phẩm chưa có trong giỏ hàng, tạo mới chi tiết giỏ hàng
            chi_tiet = ChiTietGioHang(gioHang=gio_hang.id, sachID=sach_id, soLuong=int(quantity))
            db.session.add(chi_tiet)

        db.session.commit()

        # return redirect(url_for('add_to_cart', sach_id=sach_id))
        return jsonify({"message": "Sản phẩm đã được thêm vào giỏ hàng!"})
    return render_template('productDetail.html')  # Chuyển hướng về trang giỏ hàng

    # Trả về phản hồi dưới dạng JSON (nếu cần)
    # return jsonify({"message": "Thêm vào giỏ hàng thành công", "quantity": quantity}), 200
@app.route('/payment')
def payment():
    return render_template('payment.html')


if __name__ == '__main__':
    app.run()
