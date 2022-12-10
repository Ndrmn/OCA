# from flask_sqlalchemy import SQLAlchemy
from app import db
# from datetime import timedelta


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)


class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

    # def __init__(self, **kwargs):
        # self.name = kwargs.get('user_name')


class Answer(db.Model):
    __tablename__="answers"
    id = db.Column(db.Integer, primary_key=True)
    date_of_testing = db.Column(db.DateTime, nullable=False)
    test_data = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False,index=True)
    user=db.relationship('User',backref='user_answers',foreign_keys=[user_id])
