from app import app
from flask import render_template
import untils


@app.route("/")
def index():
    sach = untils.load_book()

    return render_template('home.html', sach=sach)


if __name__ == '__main__':
    app.run()
