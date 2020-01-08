from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import Integer,String, Boolean, Text

app = Flask(__name__)
database_uri = 'postgresql+psycopg2://postgres:postgres@128.199.227.108:5432/videoserv'
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
db = SQLAlchemy(app)

class Questions(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String)
    def __init__(self,question):
        self.question = question

class Username(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String, index=True)
    videoname = db.Column(db.String, index=True, unique=True)
    def __init__(self, username,videoname):
        self.videoname = videoname
        self.username = username

class Login(db.Model):
    __tablename__ = 'login'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =  db.Column(db.String, index=True, unique=True)
    name = db.Column(db.String, index=True,unique=True)
    is_company = db.Column(db.Boolean, default=False)



    
# class Videoname(db.Model):
#     __tablename__ ='videoname'
#     id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     videoname = db.Column(db.String, index=True, unique=True)
#     def __init__(self, videoname):
#         self.videoname = videoname


db.create_all()