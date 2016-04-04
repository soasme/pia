# -*- coding: utf-8 -*-

# wsgi application: flask app
from flask import Flask
app = Flask(__name__)

# db support: flask-sqlalchemy integrated
# mq support: celery integrated
# user support: flask-user integrated
# oauth support: flask-oauthlib integrated
# default user: builtin

# route: builtin jq
# route: builtin echo
# route: setenv
# route: printenv

# route: add prog
# route: delete prog
# route: update prog
# route: get progs
# route: get prog run hist
# route: trigger prog

# errorhandler: ProgAbort
