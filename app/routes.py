# -*- coding: utf-8 -*-
from flask import request, jsonify, Response
from app import app, db
from .test_data import questions
from .models import Admin, User, Answer
from flask_jwt_extended import jwt_required, get_jwt_identity


@app.route('/api/test', methods=['GET'])
def test():
    return questions


@app.route('/api/test', methods=["post"])
def set_unswers():
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
    return [{'name': user.name, 'id': user.id} for user in User.query.all()]

# !!!!!!!!!!


@app.route('/api/user/<id_user>', methods=['DELETE'])
def delete_user(id_user):
    users = User.query.filter(User.id == id_user).all()
    if len(users) == 0:
        return jsonify({})
    user_id = users[0].id
    db.session.delete(User)
    db.session.commit()
    return jsonify({"deleted": f"{user_id}"})

# !!!!!!!!!!


@app.route('/api/get_answers/<id_user>')
def get_answers(id_user):
    users = User.query.filter(User.id == id_user).all()
    if len(users) == 0:
        return jsonify({})
    user_id = users[0].id
    answers = Answer.query.filter(Answer.user_id == user_id).all()
    return jsonify([{'test_data': answer.test_data, 'date_of_testing': str(answer.date_of_testing)} for answer in answers])


@app.route('/register', methods=['POST'])
def register():
    print(request)
    params = request.json
    admin = Admin(**params)
    db.session.add(admin)
    db.session.commit()
    token = admin.get_token()
    return {'access_token': token}


@app.route('/register', methods=['GET'])
def register_info():
    return jsonify({"info": "in post request send json whith name, password, email"})


@app.route('/login', methods=['POST'])
def login():
    params = request.json
    admin = Admin.authenticate(**params)
    token = admin.get_token()
    return {'access_token': token}


@app.route('/login', methods=["GET"])
def login_info():
    return jsonify({"info": "in post request send json whith name, password"})
