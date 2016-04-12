# -*- coding: utf-8 -*-

# wsgi application: flask app
from flask import Flask
import yaml

app = Flask(__name__)

from flask import request, make_response

from pia.blueprints.builtin import builtin
from pia.blueprints.builtin import view
app.register_blueprint(builtin, url_prefix='/builtin')

from pia.blueprints.userprogram import bp
app.register_blueprint(bp)

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

from pia.core import celery

celery.conf.update(
    BROKER_URL='redis://',
    CELERY_RESULT_BACKEND='redis://',
)



# errorhandler: ProgAbort

if __name__ == '__main__':
    app.debug = True
    app.run()
