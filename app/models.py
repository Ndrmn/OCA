from app import db
from sqlalchemy.orm import relationship
from datetime import timedelta

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False,unique=True)

class Answers(db.Model):
    __tablename__="answers"
    id=db.Column(db.Integer,primary_key=True)
    # user_id
    # test_date
    # answers
