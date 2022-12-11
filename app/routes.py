# -*- coding: utf-8 -*-
from flask import request, jsonify, Response
from app import app, db
from .test_data import questions
from .models import Admin, User, Answer
# from flask_cors import cross_origin


@app.route('/api/test', methods=['GET'])
def test():
    return questions


@app.route('/api/test', methods=["post"])
def get_unswers():
    data: dict = request.json
    user_name = data.get('user')
    if user_name:
        user = User.query.filter(User.name == user_name).first()
        if not user:
            User.addUser(user_name)
            user = User.query.filter(User.name == user_name).first()
        test_result = data.get('data')
        if test_result:
            Answer.addAnswer(user=user, test_data=test_result)

    return "get data"


@app.route('/')
def index():
    return """get_answers  GET      /api/get_answers/<user>
    get_unswers  POST     /api/test
    get_users    GET      /api/get_users
    index        GET      /
    static       GET      /static/<path:filename>
    test         GET      /api/test"""


@app.after_request
def after_request(response: Response) -> Response:
    response.access_control_allow_origin = "*"
    return response


@app.route('/api/get_users')
def get_users():
    return [user.name for user in User.query.all()]


@app.route('/api/get_answers/<user>')
def get_answers(user):
    user_id = User.query.filter(User.name == user).first().id
    answers = Answer.query.filter(Answer.user_id == user_id).all()
    return [{'test_data': answer.test_data, 'date_of_testing': answer.date_of_testing} for answer in answers]
