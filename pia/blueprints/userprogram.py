# -*- coding: utf-8 -*-

import yaml
from flask import Blueprint
from flask import request
from flask import render_template

from pia.program import async_run_pipe
from pia.models import Program
from pia.models import User
from pia.models import Env

bp = Blueprint('userprogram', __name__)

@bp.route('/<username>/<program_slug>')
def get_user_program(username, program_slug):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404)

    program = Program.query.filter_by(user_id=user.id, slug=program_slug).first()
    if not program:
        abort(404)

    envs = Env.query.filter_by(user_id=user.id).all()
    envs = {env.key: env.value for env in envs}

    if request.method == 'POST':
        code = yaml.load(program.code)
        pipe = code['pipe']
        payload = request.json
        if not payload:
            abort(400)
        async_result = async_run_pipe(payload, pipe, envs)
        if request.args.get('foreground', type=int, default=0):
            data = async_result.get(timeout=10)
            resp = make_response(json.dumps(data))
            resp.content_type = 'application/json'
            return resp
        return jsonify(task_id=async_result.id)

    return render_template(
        'userprogram/index.html',
        user=user,
        program=program,
    )
