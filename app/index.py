from __init__ import app
from flask import render_template
import untils


@app.route("/")
def index():
    sach = untils.load_book()

    return render_template('home.html', sach=sach)


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/payment')
def payment():
    return render_template('payment.html')


if __name__ == '__main__':
    app.run()
