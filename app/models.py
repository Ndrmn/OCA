# from flask_sqlalchemy import SQLAlchemy
from app import db
from datetime import timedelta
from datetime import datetime
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100),  nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(
            identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, **kwargs):
        admin = cls.query.filter(cls.name == kwargs.get('name')).one()
        if not bcrypt.verify(kwargs.get('password'), admin.password):
            raise Exception('No user with this password')
        return admin


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    dateofbirth = db.Column(db.String(20), default="1970-01-01")
    gender = db.Column(db.String(8), default="male")
    phone = db.Column(db.String(20), default="")
    email = db.Column(db.String(50), default="")
    consent = db.Column(db.String(5), default="on")
    date_of_testing = db.Column(db.DateTime)
    test_data = db.Column(db.String(600), nullable=False)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.dateofbirth = kwargs.get('dateofbirth')
        self.gender = kwargs.get('gender')
        self.phone = kwargs.get('phone')
        self.email = kwargs.get('email')
        self.consent = kwargs.get('consent')
        self.test_data = kwargs.get('test_data')
        self.date_of_testing = datetime.now()


# class Answer(db.Model):
    # __tablename__ = "answers"
    # id = db.Column(db.Integer, primary_key=True)
    # date_of_testing = db.Column(db.DateTime, nullable=False)
    # test_data = db.Column(db.String(100), nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey(
    # 'users.id'), nullable=False, index=True)
    # user = db.relationship(
    # 'User', backref='user_answers', foreign_keys=[user_id])

    # def addAnswer(**kwags):
    # answer = Answer(user=kwags.get('user'), test_data=kwags.get(
    # 'test_data'), date_of_testing=datetime.now())
    # db.session.add(answer)
    # db.session.commit()
