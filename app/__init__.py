from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__, static_folder='./static/')

app.secret_key = 'skdljfsdlfjkfljasflajsflks'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookstore?charset=utf8mb4" % quote(
    "runa@2610")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["LIST_SIZE"] = 9
app.config['COMMENT_SIZE'] =10
app.config['SECRET_KEY'] = "kldsfjhsalkfjaslfjs"




app.config["VNPAY_TMN_CODE"] = "4PJ3DKYQ"
app.config["VNPAY_PAYMENT_URL"] = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
app.config["VNPAY_HASH_SECRET_KEY"]= "ABXVSFWECOAMWENZLE2YRPA3LB0NKUM1"
app.config["VNPAY_RETURN_URL"] = "http://localhost:5000/payment_return"
db = SQLAlchemy(app)

cloudinary.config(
    cloud_name='dcrsia5sh',
    api_key='322323275186128',
    api_secret='WI88JVO5O6PfKIrFCAP3SJvIt8E'
)

loginMNG = LoginManager(app)
