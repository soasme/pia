# -*- coding: utf-8 -*-

# wsgi application: flask app
from flask import Flask
import yaml

app = Flask(__name__)

with open('.env') as f:
    ENV = yaml.load(f.read())

from flask import request, make_response
from .builtin.jq import jq, InvalidJQFilter

@app.route('/builtin/jq', methods=['POST'])
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

@app.route('/builtin/echo', methods=['POST'])
def builtin_echo():
    """
    Builtin program: `echo`.
    It will response form data.
    """
    resp = make_response(request.data)
    resp.content_type = request.content_type
    return resp

# route: setenv
# route: printenv

# route: add prog
# route: delete prog
# route: update prog
# route: get progs
# route: get prog run hist
# route: trigger prog

def _load_program(username, program):
    with open('./programs/%s/%s.yml' % (username, program)) as f:
        data = f.read()
        data = yaml.load(data)
        return data

from flask import abort, jsonify
import os
from celery import chain
from celery import Celery
import requests
import json
import logging
logging.getLogger("urllib3").setLevel(logging.DEBUG)

celery = Celery('app', broker='redis://')
celery.conf.update(
    CELERY_RESULT_BACKEND='redis://'
)

from pia.utils import formatenv

@celery.task
def prog_runner(input, prog):
    """
    A celery task to run program.
    """
    prog = formatenv(prog, ENV)
    prog['json'] = input
    prog.pop('data', None)
    method = prog.pop('method', 'post').lower()
    resp = getattr(requests, method)(**prog)
    if not resp.status_code == 200:
        return json.dumps({'message': resp.content}), 400
    try:
        return resp.json()
    except:
        return {'_': resp.content}

@app.route('/<username>/<program>', methods=['POST'])
def run_prog(username, program):
    """
    Run a pipe program
    """
    detach = request.args.get('detach')
    program = _load_program(username, program)
    pipe = program['pipe']
    tasks = []
    if not pipe:
        abort(400)
    tasks.append(prog_runner.s(request.json, pipe[0]))
    for prog in program['pipe'][1:]:
        tasks.append(prog_runner.s(prog))
    res = chain(*tasks)()
    if detach:
        return jsonify(state='triggered')
    try:
        data = res.get(timeout=30)
    except Exception as e:
        raise e
    resp = make_response(json.dumps(data))
    resp.content_type = 'application/json'
    return resp

# errorhandler: ProgAbort

if __name__ == '__main__':
    app.debug = True
    app.run()
