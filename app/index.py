from app import app
from flask import render_template
import untils


@app.route("/")
def index():
    sach = untils.load_book()
    theLoai = untils.load_category()
    return render_template('home.html', sach=sach, category=theLoai)

@app.route("/login")
def login():
    theLoai = untils.load_category()
    return render_template('login.html', category=theLoai)
if __name__ == '__main__':
    app.run()
