# -*- coding: utf-8 -*-
from flask import request, jsonify, Response
from app import app, db
from .test_data import questions
from .models import Admin, User, Answer
from datetime import datetime
# from flask_cors import cross_origin


@app.route('/test', methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def test():
    return questions


@app.route('/test', methods=["post"])
def get_unswers():
    data: dict = request.json
    user_name = data.get('user')
    if user_name:
        user = User.query.filter(User.name == user_name).first()
        if not user:
            user = User(name=user_name)
            db.session.add(user)
            db.session.commit()
            print(f'user {user_name} id added')
            user = User.query.filter(User.name == user_name).first()
        test_result = data.get('data')
        if test_result:
            answer = Answer(user=user, test_data=test_result,
                            date_of_testing=datetime.now())
            db.session.add(answer)
            db.session.commit()

    return "get data"


@app.route('/')
def index():
    return "/test, /admin -not realased"


@app.after_request
def after_request(response: Response) -> Response:
    response.access_control_allow_origin = "*"
    return response
