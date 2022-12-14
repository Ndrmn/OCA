# -*- coding: utf-8 -*-
from flask import request, jsonify, Response, send_file
import io
import urllib
import base64
from app import app, db
from .testing_logic import questions, test_results
from .models import Admin, User, Answer
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from .graph import render_graph


def form_data_parser(data):
    data_list = data.decode('utf-8').split('\r\n')
    user_data = dict()
    user_answers = list()
    for data_el in data_list:
        if len(data_el):
            if data_el.find('question') == 0:
                user_answers.append(data_el.split('=')[1])
            else:
                key, value = data_el.split('=')
                if len(key):
                    user_data[key] = value

    return {'user': user_data, 'data': user_answers}


@app.route('/api/test', methods=['GET'])
def test():
    return questions


@app.route('/api/test', methods=["POST", "OPTIONS"])
def set_answers():
    try:
        data: dict = form_data_parser(request.data)
    except:
        try:
            data: dict = json.loads(request.data)
        except:
            return "no match data"
    user_params = data.get('user')
    if user_params:
        user = User.query.where((User.name == user_params.get(
            'name')) & (User.surname == user_params.get('surname'))).first()
        if not user:
            user = User(**user_params)
            db.session.add(user)
            db.session.commit()
            user = User.query.where((User.name == user_params.get(
                'name')) & (User.surname == user_params.get('surname'))).first()
        Answer.addAnswer(user=user, test_data=','.join(data.get('data')))

        return "get data"
    return '"not match data: waiting {user:user_data, data:answers_arr}"'


@app.route('/')
def index():
    url_of_api = """
    <p>Endpoint       Methods  Rule</p>
    <br>delete_user    DELETE   /api/user/<id_user>
    <br>get_answers    GET      /api/get_answers/<id_user>
    <br>get_users      GET      /api/get_users
    <br>index          GET      /
    <br>login          POST     /login
    <br>login_info     GET      /login
    <br>register       POST     /register
    <br>register_info  GET      /register
    <br>set_unswers    POST     /api/test
    <br>static         GET      /static/<path:filename>
    <br>test           GET      /api/test
    """
    return url_of_api


@app.route('/api/get_users')
def get_users():
    return [{'id': user.id, "name": user.name, "surname": user.surname, 'gender': user.gender, 'email': user.email} for user in User.query.all()]


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
        return {"no user": f"{id_user}"}
    user_id = users[0].id
    answers = Answer.query.filter(Answer.user_id == user_id).all()
    return jsonify([{'id of test result ': answer.id, 'test_data': answer.test_data, 'date_of_testing': str(answer.date_of_testing)} for answer in answers])


@app.route('/api/get_test_graph/<id>')
def get_test_graph(id):
    answer = Answer.query.filter(Answer.id == id).all()
    if len(answer):
        full_answer = db.session.query(Answer, User).select_from(
            Answer).join(User).filter(Answer.id == id).all()
        test_results_data = test_results(
            age=14, gender=full_answer[0][1].gender, input_answers_str=full_answer[0][0].test_data)
        # age!
        fig = render_graph(test_data=test_results_data.get(
            'allPercents'), answer197=test_results_data.get('anwser197'), answer22=test_results_data.get('answer22'), notSureFlag=test_results_data.get('notSureFlag'))

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        html = '<img src = "%s"/>' % uri

        return html


@app.route('/api/get_test_result/<id>')
def get_test_result(id):
    answer = Answer.query.filter(Answer.id == id).all()
    if len(answer):
        full_answer = db.session.query(Answer, User).select_from(
            Answer).join(User).filter(Answer.id == id).all()
        return test_results(age=14, gender=full_answer[0][1].gender, input_answers_str=full_answer[0][0].test_data)
        # age!
    return {}


@ app.route('/register', methods=['POST'])
def register():
    try:
        # print(request)
        params = request.json
        if Admin.query.filter(Admin.name == params.get('name')).all():
            return {"user whith this name is present": "please choose another name for user"}
        admin = Admin(**params)
        db.session.add(admin)
        db.session.commit()
        token = admin.get_token()
        return {'access_token': token}
    except:
        return {"error": "bad request"}


@ app.route('/register', methods=['GET'])
def register_info():
    return jsonify({"info": "in post request send json whith name, password, email"})


@ app.route('/login', methods=['POST'])
def login():
    try:
        params = request.json
        admin = Admin.authenticate(**params)
        token = admin.get_token()
        return {'access_token': token}
    except:
        return {"error": "bad request"}


@ app.route('/login', methods=["GET"])
def login_info():
    return jsonify({"info": "in post request send json whith name, password"})


@ app.after_request
def after_request(response: Response) -> Response:
    response.access_control_allow_origin = "*"
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
