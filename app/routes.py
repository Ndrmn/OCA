# -*- coding: utf-8 -*-
from flask import request, jsonify, Response, send_file
import flask
import io
import urllib
import base64
from app import app, db
from .testing_logic import questions, test_results
from .models import Admin, User
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from .graph import render_graph
import datetime


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
    user_data['test_data'] = ','.join(user_answers)

    return user_data


@app.route('/api/test', methods=['GET'])
# @jwt_required()
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
    # andrey stup
    user = User(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return "no match data"
    # andrey stup
    # user_params = data.get('user')
    # if user_params:

    # user = User.query.where((User.name == user_params.get(
    # 'name')) & (User.surname == user_params.get('surname'))).first()
    # if not user:
    # user = User(**user_params)
    # db.session.add(user)
    # db.session.commit()
    # user = User.query.where((User.name == user_params.get(
    # 'name')) & (User.surname == user_params.get('surname'))).first()
    # Answer.addAnswer(user=user, test_data=','.join(data.get('data')))

    # return "get data"
    # return '"not match data: waiting {user:user_data, data:answers_arr}"'
    return "get data"


@app.route('/')
def index():
    return flask.render_template('/index.html')


@app.route('/api/get_users')
def get_users():
    result = []

    for user in User.query.all():

        # user_id = user.id
        # answers_from_user = Answer.query.filter(
        # Answer.user_id == user_id).all()
        answers = []
        # for answer in answers_from_user:

        # answers.append({'id of test graph': answer.id,
        #    'date_of_testing': str(answer.date_of_testing)})

        user_data = {'id': user.id, "name": user.name, "surname": user.surname, 'gender': user.gender, 'email': user.email,
                     "dateofbirth": user.dateofbirth, "phone": user.phone, "date_of_testing": user.date_of_testing, "test_data": user.test_data, 'answers': answers}

        result.append(user_data)

    return result


# @ app.route('/api/get_answers/<id_user>')
# def get_answers(id_user):
    # users = User.query.filter(User.id == id_user).all()
    # if len(users) == 0:
    # return {"no user": f"{id_user}"}
    # user_id = users[0].id
    # answers = Answer.query.filter(Answer.user_id == user_id).all()
    # return jsonify([{'id of test result ': answer.id, 'test_data': answer.test_data, 'date_of_testing': str(answer.date_of_testing)} for answer in answers])


@ app.route('/api/get_test_graph/<id>')
def get_test_graph(id):
    user = User.query.filter(User.id == id).all()
    if len(user):

        # full_answer = db.session.query(Answer, User).select_from(
        # Answer).join(User).filter(Answer.id == id).all()
        # test_results_data = test_results( age=14, gender=full_answer[0][1].gender, input_answers_str=full_answer[0][0].test_data)
        date_of_bitth = datetime.datetime.strptime(
            user[0].dateofbirth, "%Y-%m-%d").date()
        date_of_testing = user[0].date_of_testing
        age = date_of_testing.year - date_of_bitth.year
        if date_of_testing.month < date_of_bitth.month or (date_of_testing.month == date_of_bitth.month and date_of_testing.day < date_of_bitth.day):
            age -= 1
        test_results_data = test_results(
            age=age, gender=user[0].gender, input_answers_str=user[0].test_data)
        fig = render_graph(test_data=test_results_data.get(
            'allPercents'), answer197=test_results_data.get('answer197'), answer22=test_results_data.get('answer22'), notSureFlag=test_results_data.get('notSureFlag'))

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())

        uri = 'data:image/png;base64,' + urllib.parse.quote(string)
        html = '<img src = "%s"/>' % uri

        return html
    return {}


# @ app.route('/api/get_test_result/<id>')
# def get_test_result(id):
    # answer = Answer.query.filter(Answer.id == id).all()
    # if len(answer):
    # full_answer = db.session.query(Answer, User).select_from(
    # Answer).join(User).filter(Answer.id == id).all()
    # return test_results(age=14, gender=full_answer[0][1].gender, input_answers_str=full_answer[0][0].test_data)
    # age!
    # return {}


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
        return {'access_token': token, 'token_live_date': datetime.datetime.now() + datetime.timedelta(hours=24)}
    except:
        return {"error": "bad request"}


# @ app.route('/register', methods=['GET'])
# def register_info():
    # return jsonify({"info": "in post request send json whith name, password, email"})


@ app.route('/test_auth_api', methods=['POST'])
@ jwt_required()
def test_auth_api():
    return {'you are logged succesfulli': 'ok'}


@ app.route('/login', methods=['POST'])
def login():
    try:
        params = request.json
        admin = Admin.authenticate(**params)
        token = admin.get_token()
        return {'access_token': token, 'token_live_date': datetime.datetime.now() + datetime.timedelta(hours=24)}
    except:
        return {"error": "bad request"}


# @ app.route('/login', methods=["GET"])
# def login_info():
    # return jsonify({"info": "in post request send json whith name, password"})


@ app.after_request
def after_request(response: Response) -> Response:
    response.access_control_allow_origin = "*"
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response
