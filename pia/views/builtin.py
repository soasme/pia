# -*- coding: utf-8 -*-

from flask import request
from flask import make_response
from flask import jsonify
from flask import Blueprint

from ..builtin.jq import jq, InvalidJQFilter

bp = Blueprint('builtin', __name__)

@bp.route('/jq', methods=['POST'])
def builtin_jq():
    """
    Builtin program: `jq`.
    It will run a `jq` progress and return a json object.
    """
    program = request.args.get('program', ".")
    command = request.data
    try:
        data = jq(program, command)
        resp = make_response(data)
        resp.content_type = 'application/json'
        return resp
    except InvalidJQFilter as exception:
        return jsonify(message=str(exception)), 400

@bp.route('/echo', methods=['POST'])
def builtin_echo():
    """
    Builtin program: `echo`.
    It will response form data.
    """
    resp = make_response(request.data)
    resp.content_type = request.content_type
    return resp
