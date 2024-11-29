import math, utils, cloudinary.uploader
from app import app, loginMNG
from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user


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
    size = app.config['LIST_SIZE']
    start = (page - 1) * size
    end = start + size

    books = utils.get_list_books(cate_id)[start:end]
    l = len(utils.get_list_books(cate_id))
    return render_template('products.html',
                           page=math.ceil(len(utils.get_list_books(cate_id)) / app.config['LIST_SIZE']),
                           lb=books)


@app.route("/register", methods=['GET', 'POST'])
def register():
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


if __name__ == '__main__':
    app.run()
