# -*- coding: utf-8 -*-
from flask import request, jsonify
from app import app, db
from .test_data import questions


@app.route('/test', methods=['GET'])
def test():
    # return jsonify(questions)
    return jsonify(questions)


@app.route('/test', methods=["POST"])
def get_unswers():
    # print(request.json)
    return "get data"

@app.route('/')
def index():
    return "/test, /admin -not realased"
