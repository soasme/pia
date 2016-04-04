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
from flask import request, make_response
@app.route('/builtin/jq', methods=['POST'])
def builtin_jq():
    """
    Builtin program: `jq`.
    It will run a `jq` progress and return a json object.
    """
    import subprocess
    program = request.args.get('program', ".")
    data = request.data
    prog = subprocess.Popen(['jq', program], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = prog.communicate(input=data)
    resp = make_response(out)
    resp.content_type = 'application/json'
    return resp

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

if __name__ == '__main__':
    app.debug = True
    app.run()
