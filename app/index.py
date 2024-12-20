import math, utils, cloudinary.uploader, admin, hashlib, os
import json
import docx
from models import *
from __init__ import app, loginMNG, db
from flask import render_template, request, redirect, url_for, jsonify, flash, send_file, Flask
from docx import Document
from sqlalchemy import func
from flask_login import login_user, logout_user, current_user, login_required
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


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
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    check = checkAuthenticated()
    if check:
        return check
    checkAuthenticated()
    return render_template('profile.html')


@app.route('/changeProfile', methods=['GET', 'POST'])
@login_required
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

        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('changeProfile.html')


@app.route("/changePassword", methods=['GET', 'POST'])
@login_required
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


@app.route("/products/<int:sach_id>", methods=['GET','POST'])
def productDetail(sach_id):
    book = utils.get_book_by_id(sach_id)
    if request.method == 'POST':
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
            ChiTietGioHang.sach == sach_id).first() # Đảm bảo `sach` là một đối tượng

        if chi_tiet:
            # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng lên
            chi_tiet.soLuong += int(quantity)
        else:
            # Nếu sản phẩm chưa có trong giỏ hàng, tạo mới chi tiết giỏ hàng
            chi_tiet = ChiTietGioHang(gioHang=gio_hang.id, sach=sach_id, soLuong=int(quantity))
            db.session.add(chi_tiet)

        db.session.commit()

        # return redirect(url_for('add_to_cart', sach_id=sach_id))
        return jsonify({"message": "Sản phẩm đã được thêm vào giỏ hàng!"})
    return render_template('productDetail.html', sach=book)
@app.route("/paymentNow", methods=['POST'])
def paymentNow():
    if not current_user.is_authenticated:
        return jsonify({"error": "Bạn cần đăng nhập để thanh toán."}), 401

    if request.method == 'POST':
        try:
            # Lấy dữ liệu từ body của yêu cầu
            data = request.get_json()
            print("Dữ liệu nhận được:", data)

            product = data.get('quantity')  # Giá trị mặc định nếu không có

            # Tạo đơn hàng
            don_hang = DonHang(nguoiDung=current_user.id)
            db.session.add(don_hang)
            db.session.commit()

            sach_id = product.get('id')
            quantity = product.get('quantity', 1)

            chi_tiet = ChiTietDonHang(
                id_DonHang=don_hang.id,
                id_Sach=sach_id,
                soLuong=int(quantity)
            )
            db.session.add(chi_tiet)

            db.session.commit()

            return jsonify({"message": "Thanh toán thành công!", "donHangId": don_hang.id})
        except Exception as e:
            print("Lỗi:", e)
            return jsonify({"error": str(e)}), 500
    return render_template('payment.html')
#note


@app.route("/import", methods=['GET', 'POST'])
@login_required
def import_book():
    check = checkImporter()
    if check:
        return check
    page = int(request.args.get('page', 1))
    size = 5
    start = (page - 1) * size
    end = start + size
    list_import = db.session.query(PhieuNhapSach.id, PhieuNhapSach.ngayNhapSach,
                                   NguoiDung.hoVaTen.label('hoVaTen')).join(NguoiDung,
                                                                            NguoiDung.id == PhieuNhapSach.id_NguoiDung).order_by(
        PhieuNhapSach.id.desc()).all()
    l = len(list_import)
    current_page = int(request.args.get('page', 1))
    list_import = list_import[start:end]
    list_import_detail = []
    selected_import = None

    if request.method == 'POST':
        data = request.json
        id_import = data.get('id_Import')
        if id_import:
            selected_import = utils.get_import_by_id(int(id_import))
            list_import_detail = db.session.query(
                ChiTietNhapSach.soLuong,
                Sach.ten.label("ten_sach"),
                Sach.tacGia.label("tac_gia"),
                TheLoai.ten.label("ten_the_loai")
            ).join(
                Sach, ChiTietNhapSach.id_Sach == Sach.id
            ).join(
                TheLoai, Sach.id_TheLoai == TheLoai.id
            ).filter(
                ChiTietNhapSach.id_PhieuNhapSach == id_import
            ).all()

            details = [{
                "ten_sach": ct.ten_sach,
                "ten_the_loai": ct.ten_the_loai,
                "tac_gia": ct.tac_gia,
                "soLuong": ct.soLuong
            } for ct in list_import_detail]

            return jsonify({
                "success": True,
                "details": details,
                "ngay_nhap": selected_import.ngayNhapSach.strftime('%d-%m-%Y') if selected_import else None
            })
        return jsonify({"success": False}), 400

    return render_template('import_home.html',
                           selected_import=selected_import,
                           list_import=list_import,
                           list_import_detail=list_import_detail,
                           page=math.ceil(l / 5),
                           current_page=current_page)


@app.route('/importCreate', methods=['GET', 'POST'])
@login_required
def create_import():
    check = checkImporter()
    if check:
        return check
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
        qd = utils.get_qd()
        return render_template('create_import.html', today=datetime.now().strftime('%Y-%m-%d'), quy_dinh=qd)

    elif request.method == 'POST':
        data = request.json
        ngay_nhap = data.get('ngayNhap')
        sach_list = data.get('sachList', [])
        phieu_nhap = PhieuNhapSach.query.filter(PhieuNhapSach.ngayNhapSach == ngay_nhap).first()
        if not phieu_nhap:
            db.session.add(PhieuNhapSach(ngayNhapSach=ngay_nhap, id_NguoiDung=current_user.id))
            db.session.commit()
            phieu_nhap = PhieuNhapSach.query.filter(PhieuNhapSach.ngayNhapSach == ngay_nhap).first()
        for sach in sach_list:
            chi_tiet = ChiTietNhapSach(
                soLuong=sach['soLuong'],
                id_Sach=sach['id_Sach'],
                id_PhieuNhapSach=phieu_nhap.id
            )
            db.session.add(chi_tiet)

            sach_obj = Sach.query.get(sach['id_Sach'])
            sach_obj.soLuongTonKho += sach['soLuong']

        db.session.commit()

        return jsonify({'success': True})


@app.route('/addBook', methods=['GET', 'POST'])
@login_required
def add_book():
    check = checkImporter()
    if check:
        return check
    err_msg = ''
    suc_msg = ''
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
                       , id_TheLoai=id_TheLoai, image=image_path)
        flash('Đã thêm sách thành công.', 'success')
        return redirect(url_for('add_book'))
    theLoaiList = TheLoai.query.all()
    return render_template('add_book.html', theLoaiList=theLoaiList)


@app.route('/bill', methods=['GET', 'POST'])
@login_required
def bill():
    check = checkEmployee()
    if check:
        return check
    page = int(request.args.get('page', 1))
    size = app.config['LIST_SIZE']
    start = (page - 1) * size
    end = start + size
    id_bill = None
    list_bill = db.session.query(DonHang.id.label('id_don_hang'),
                                 DonHang.ngayDatHang.label('ngay_dat_hang'),
                                 DonHang.phuongThucThanhToan.label('pttt'),
                                 NguoiDung.hoVaTen.label('ten_user'),
                                 DonHang.trangThai.label('trang_thai'),
                                 func.sum(Sach.donGia * ChiTietDonHang.soLuong).label('tong_gia')) \
        .select_from(DonHang).join(ChiTietDonHang, DonHang.id == ChiTietDonHang.id_DonHang) \
        .join(Sach, ChiTietDonHang.id_Sach == Sach.id) \
        .join(NguoiDung, DonHang.nguoiDung == NguoiDung.id) \
        .group_by(DonHang.id, DonHang.ngayDatHang, DonHang.phuongThucThanhToan, NguoiDung.hoVaTen,
                  DonHang.trangThai).order_by(DonHang.id.desc()).all()
    l = len(list_bill)
    current_page = int(request.args.get('page', 1))
    list_bill = list_bill[start:end]
    selected_bill = None
    list_bill_detail = []
    if request.method=='POST':
        data=request.json
        id_bill=data.get('id_Bill')
        if id_bill:
            selected_bill = utils.get_bill_by_id(int(id_bill))
            list_bill_detail = db.session.query(ChiTietDonHang.soLuong, Sach.ten.label("ten_sach"),
                                                Sach.tacGia.label("tac_gia"), TheLoai.ten.label("ten_the_loai")) \
                .join(Sach, ChiTietDonHang.id_Sach == Sach.id) \
                .join(TheLoai, Sach.id_TheLoai == TheLoai.id) \
                .filter(ChiTietDonHang.id_DonHang == id_bill) \
                .all()
        details = [{
            "ten_sach": ct.ten_sach,
            "ten_the_loai": ct.ten_the_loai,
            "tac_gia": ct.tac_gia,
            "soLuong": ct.soLuong
        } for ct in list_bill_detail]

        return jsonify({
            "success": True,
            "details": details,
            "ngay_dat_hang": selected_bill.ngayDatHang.strftime('%d-%m-%Y') if selected_bill else None
        })
    return render_template('bill_home.html', list_bill=list_bill,
                           selected_bill=selected_bill, list_bill_detail=list_bill_detail,
                           page=math.ceil(l / app.config['LIST_SIZE']),
                           current_page=current_page)


@app.route('/billCreate', methods=['GET', 'POST'])
@login_required
def create_bill():
    check = checkEmployee()
    if check:
        return check
    if request.method == 'GET':
        id = request.args.get('id')
        if id:
            books = Sach.query.filter(Sach.id == int(id)).all()
            results = [
                {
                    'id': book.id,
                    'ten': book.ten,
                    'theLoai': book.TheLoai.ten,
                    'donGia': book.donGia
                }
                for book in books
            ]
            return jsonify(results)
        return render_template('create_bill.html', today=datetime.today().date())
    elif request.method == 'POST':
        data = request.json
        ngay_lap_hoa_don = data.get('ngayDatHang')
        sach_list = data.get('sachList', [])

        hoa_don = DonHang(
            ngayDatHang=ngay_lap_hoa_don,
            ngayThanhToan=ngay_lap_hoa_don,
            trangThai=TrangThai.DA_NHAN_HANG,
            phuongThucThanhToan=PhuongThucThanhToan.TRUC_TIEP,
            nguoiDung=current_user.id
        )
        db.session.add(hoa_don)
        db.session.flush()

        for p in sach_list:
            chi_tiet = ChiTietDonHang(
                id_Sach=p['id_Sach'],
                id_DonHang=hoa_don.id,
                soLuong=p['soLuong']
            )
            db.session.add(chi_tiet)

            sach_obj = utils.get_book_by_id(p['id_Sach'])
            sach_obj.soLuongTonKho -= p['soLuong']

        db.session.commit()

        return jsonify({"success": True})


@app.route('/billExport', methods=['POST'])
@login_required
def export_bill():
    data = request.json
    ngay_dat_hang = data.get('ngayDatHang')
    id = len(utils.get_bill()) + 1
    sach_list = data.get('sachList', [])
    ten_kh = data.get('ten_kh')
    tongTien = 0
    document = Document()
    document.add_heading('Hóa đơn bán sách', level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph(f'Mã hóa đơn: {id}').alignment = WD_ALIGN_PARAGRAPH.RIGHT
    document.add_paragraph(f'Tên khách hàng: {ten_kh}')
    document.add_paragraph(f'Ngày lập hóa đơn: {ngay_dat_hang}')

    table = document.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Mã sách'
    hdr_cells[1].text = 'Tên sách'
    hdr_cells[2].text = 'Thể loại'
    hdr_cells[3].text = 'Đơn giá'
    hdr_cells[4].text = 'Số lượng'

    for sach in sach_list:
        book = utils.get_book_by_id(sach['id_Sach'])
        row_cells = table.add_row().cells
        row_cells[0].text = str(book.id)
        row_cells[1].text = book.ten
        row_cells[2].text = book.TheLoai.ten
        row_cells[3].text = f"{book.donGia:,} VND"
        row_cells[4].text = str(sach['soLuong'])
        tongTien += book.donGia * sach['soLuong']

    for row in table.rows:
        for cell in row.cells:
            # Đảm bảo tất cả các ô có viền
            cell._element.get_or_add_tcPr().append(
                parse_xml(
                    f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:space="0" w:color="000000" w:sz="4"/><w:left w:val="single" w:space="0" w:color="000000" w:sz="4"/><w:bottom w:val="single" w:space="0" w:color="000000" w:sz="4"/><w:right w:val="single" w:space="0" w:color="000000" w:sz="4"/></w:tcBorders>'
                )
            )

    os.makedirs('exports', exist_ok=True)

    document.add_paragraph(f'Thành tiền: {tongTien}')

    # Lưu file vào server
    file_name = f'HoaDon_{id}.docx'
    file_path = os.path.join('exports', file_name)
    document.save(file_path)

    # Trả về đường dẫn tải file
    download_url = url_for('download_file', filename=file_name, _external=True)
    return jsonify({
        'success': True,
        'download_url': download_url
    })


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'exports/{filename}', as_attachment=True)


def checkAuthenticated():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))


def checkEmployee():
    if not current_user.is_authenticated or not current_user.is_employee():
        return redirect(url_for('index'))


def checkImporter():
    if not current_user.is_authenticated or not current_user.is_importer():
        return redirect(url_for('index'))


@app.route('/cart', methods=['GET','POST'])
def cart():
    if not current_user.is_authenticated:
        return redirect('/login')
        # Giả sử bạn lấy đơn hàng từ database dựa trên user_id
    current_user_id = current_user.id  # ID người dùng hiện tại (nếu có đăng nhập)

    # lấy giỏ hàng của người dùng đang đăng nhập hiện tại ( mỗi người chỉ có 1 giỏ hàng)
    gio_hang = GioHang.query.filter_by(nguoiDung=current_user_id).first()
    if not gio_hang:
        return render_template('cart.html', carts=[])  # nếu giỏ hàng rỗng thì trả về rỗng
    # lấy danh sách chi tiết giỏ hàng của người dùng
    chi_tiet_GH = ChiTietGioHang.query.filter_by(gioHang=gio_hang.id).all()

    danh_sach_sach = []
    for chi_tiet in chi_tiet_GH:
        danh_sach_sach.append({
            'id': chi_tiet.Sach.id,
            'image': chi_tiet.Sach.image,
            'ten': chi_tiet.Sach.ten,
            'tacGia': chi_tiet.Sach.tacGia,
            'soLuong': chi_tiet.soLuong,
            'donGia': chi_tiet.Sach.donGia,
            'tongTien': chi_tiet.soLuong * chi_tiet.Sach.donGia,  # Tính tổng tiền
        })
    # Truyền dữ liệu vào template giỏ hàng
    return render_template('cart.html', carts=danh_sach_sach)


@app.route('/products/<int:sach_id>', methods=['POST'])
def add_to_cart(sach_id):
    return render_template('productDetail.html')  # Chuyển hướng về trang giỏ hàng

@app.route('/payment', methods=['GET','POST'])
@login_required
def payment():
    # Kiểm tra Content-Type
    if not request.is_json:
        return jsonify({"error": "Dữ liệu gửi lên không đúng định dạng JSON"}), 415
    if request.method == 'POST':
        products= []
        data = request.get_json()  # Lấy dữ liệu JSON từ body của POST request
        print("Data received:", data)

        # Lấy giá trị của `products`
        raw_products = data.get('products', '[]')  # Lấy giá trị mặc định là chuỗi '[]'

        try:
            # Parse chuỗi JSON thành danh sách Python
            products = json.loads(raw_products)
            print("Parsed products:", products)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        # lây pttt
        paymentMethod = products[0].get('paymentMethod','TRUC_TIEP')
        if paymentMethod == 'TRUC_TIEP':
            paymentMethod = PhuongThucThanhToan.TRUC_TIEP
        else:
            paymentMethod = PhuongThucThanhToan.TRUC_TUYEN
        don_hang = DonHang(nguoiDung=current_user.id, phuongThucThanhToan=paymentMethod)
        db.session.add(don_hang)
        db.session.commit()
        for pro in products:
            if isinstance(pro, dict):  # Đảm bảo mỗi phần tử là dictionary
                sach_id = pro.get('id')
                quantity = pro.get('quantity')
                if pro.get('paymentMethod') == 'Thanh toán trực tiếp':
                    paymentMethod = 'TRUC_TIEP'
                if pro.get('paymentMethod') == 'Thanh toán Momo':
                    paymentMethod = 'TRUC_TUYEN'
                print(f"sach_id: {sach_id}, quantity: {quantity}")
                chi_tiet = ChiTietDonHang(id_DonHang=don_hang.id, id_Sach=sach_id, soLuong=int(quantity))
                db.session.add(chi_tiet)
                db.session.commit()
            else:
                print("Invalid product data:", pro)
        print(don_hang.id)
        return jsonify({"message": "Thanh toán thành công!", "donHangId": don_hang.id})
    return render_template('payment.html')
    # don_hang = DonHang.query.filter_by(nguoiDung=current_user.id).order_by(
    #     DonHang.id.desc()).first()  # Lấy đơn hàng mới nhất của người dùng
    # chi_tiet_DH = ChiTietDonHang.query.filter_by(id_DonHang=don_hang.id).all()
    #
    # danh_sach_sach = []
    # for chi_tiet in chi_tiet_DH:
    #     danh_sach_sach.append({
    #         'id': chi_tiet.Sach.id,
    #         'image': chi_tiet.Sach.image,
    #         'ten': chi_tiet.Sach.ten,
    #         'tacGia': chi_tiet.Sach.tacGia,
    #         'soLuong': chi_tiet.soLuong,
    #         'donGia': chi_tiet.Sach.donGia,
    #         'tongTien': chi_tiet.soLuong * chi_tiet.Sach.donGia,  # Tính tổng tiền
    #     })
    # print(danh_sach_sach)


@app.route('/test')
def test():
    return render_template('sign_in.html')


if __name__ == '__main__':
    app.run()
