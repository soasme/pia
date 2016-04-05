# -*- coding: utf-8 -*-

# wsgi application: flask app
from flask import Flask
import yaml

app = Flask(__name__)

with open('.env') as f:
    ENV = yaml.load(f.read())

from flask import request, make_response
from .views import builtin_bp

app.register_blueprint(builtin_bp, url_prefix='/builtin')

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
import requests
import json
import logging
logging.getLogger("urllib3").setLevel(logging.DEBUG)

from .core import celery

celery.conf.update(
    BROKER_URL='redis://',
    CELERY_RESULT_BACKEND='redis://',
)


from .program import async_run_pipe

@app.route('/<username>/<program>', methods=['POST'])
def run_prog(username, program):
    """
    Run a pipe program
    """
    foreground = request.args.get('foreground', type=int, default=0)

    program = _load_program(username, program)
    pipe = program['pipe']
    if not pipe:
        abort(400)

    async_result = async_run_pipe(request.json, program['pipe'], ENV)

    if foreground:
        data = async_result.get(timeout=60)
        resp = make_response(json.dumps(data))
        resp.content_type = 'application/json'
        return resp

    return jsonify(task_id=async_result.id)


# errorhandler: ProgAbort

if __name__ == '__main__':
    app.debug = True
    app.run()
