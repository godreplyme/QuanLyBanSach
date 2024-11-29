from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key='skdljfsdlfjkfljasflajsflks'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:vrain2403@localhost/bookstore?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["LIST_SIZE"] = 9

db = SQLAlchemy(app)

cloudinary.config(
    cloud_name='dcrsia5sh',
    api_key='322323275186128',
    api_secret='WI88JVO5O6PfKIrFCAP3SJvIt8E'
)

loginMNG = LoginManager(app)
