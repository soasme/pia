# -*- coding: utf-8 -*-
"""
pia.program
~~~~~~~~~~~~~~~~~~

Implement program based on requests.
"""

import requests

from celery import chain

from .utils import formatenv
from .core import celery

RUNNERS = {
    'get': requests.get,
    'post': requests.post,
    'put': requests.put,
    'delete': requests.delete,
    'patch': requests.patch,
}


class ServerError(Exception):
    """An exception of program run abnormally on server."""
    pass


class ServerReject(Exception):
    """An exception of program got rejected by server,
    normally because of bad request, not authorized, forbidden, etc.
    """
    pass


class BrokenProgram(Exception):
    """An exception of program not configured correctly."""
    pass


class CallFailed(Exception):
    """An exception of program call failed.

    The reasons are normally in a wide range."""
    pass


def sync_run_job(jsondata, program, env=None):
    """
    Run an HTTP job.

    :param jsondata: a dictionary that will be sent as request body.
    :param program: a dictionary that defined request meta and parameter.
    :param env: a dictionary that contained environments.
    :return: return the last response that created by pipe.
    """
    env = env or {}

    # scan env placeholder in program definition
    prog = formatenv(program, env)

    # only support json request now ;)
    # other request type will be supported in the future.
    prog['json'] = jsondata
    prog.pop('data', None)

    # read method from program definition
    method = prog.pop('method', 'post').lower()
    if method not in RUNNERS:
        raise BrokenProgram('unknown method: %s' % method)

    # request data from server
    try:
        resp = RUNNERS[method](**prog)
    except TypeError as exception:
        raise BrokenProgram(str(exception))
    except requests.ConnectionError:
        raise CallFailed("connection error")

    # handle response
    if resp.status_code >= 500:
        raise ServerError(resp.content)
    elif 400 <= resp.status_code < 500:
        raise ServerReject(resp.content)
    # better to track 30x response.
    elif resp.headers['content-type'].startswith('application/json'):
        return resp.json()
    # transform none-json data to dict
    else:
        return {'_': resp.content}


@celery.task
def async_run_job(jsondata, program, env):
    """ Run job asynchronously.

    :param jsondata: a dictionary that will be sent as request body.
    :param program: a dictionary that defined request meta and parameter.
    :param env: a dictionary that contained environments.
    :return: AsyncResult, a celery task.
    """
    return sync_run_job(jsondata, program, env)


def sync_run_pipe(jsondata, programs, env=None):
    """ Run an sequence of jobs synchronously.

    :param jsondata: a dictionary that will be sent as request body.
    :param program: a dictionary that defined request meta and parameter.
    :param env: a dictionary that contained environments.
    :return: return the last response that created by pipe.
    """
    env = env or {}

    # run job in a row
    stream = jsondata
    for program in programs:
        job_response = sync_run_job(stream, program['pipe'], env)
        stream = job_response

    # return last response as pipe result
    return stream


def async_run_pipe(jsondata, programs, env=None):
    """ Run an sequence of jobs asynchronously.

    :param jsondata: a dictionary that will be sent as request body.
    :param program: a dictionary that defined request meta and parameter.
    :param env: a dictionary that contained environments.
    :return: AsyncResult, a chaining celery task.
    """
    env = env or {}

    # assemble celery tasks
    tasks = []
    tasks.append(async_run_job.s(jsondata, programs[0], env))
    for prog in programs[1:]:
        tasks.append(async_run_job.s(prog, env))

    # chaining run jobs using celery
    return chain(*tasks)()
