import math,utils
from app import app,admin
from flask import render_template, request


@app.route("/")
def index():
    return render_template('home.html', sach=utils.get_book_home(), category=utils.get_category())


@app.route("/login")
def login():
    return render_template('login.html', category=utils.get_category(), active_tab=request.args.get('tab','login'))


@app.route("/products")
def list_book():
    cate_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))
    size = app.config['LIST_SIZE']
    start = (page - 1) * size
    end = start + size

    books = utils.get_list_books(cate_id)[start:end]
    l=len(utils.get_list_books(cate_id))
    return render_template('products.html',
                           page=math.ceil(len(utils.get_list_books(cate_id)) / app.config['LIST_SIZE']),
                           lb=books, category=utils.get_category())


@app.route("/register")
def register():
    pass

if __name__ == '__main__':
    app.run()
