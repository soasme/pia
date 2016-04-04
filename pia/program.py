# -*- coding: utf-8 -*-
"""
pia.program
~~~~~~~~~~~~~~~~~~

Implement program based on requests.
"""

import requests

from .utils import formatenv


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


def run_job(jsondata, program, env=None):
    """
    Run an HTTP job.
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
