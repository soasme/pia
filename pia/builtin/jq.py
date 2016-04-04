# -*- coding: utf-8 -*-

import subprocess


class InvalidJQFilter(Exception):
    """An exception of jq parse program failed. """
    pass


def jq(program, command):
    """
    Run jq command.

    Reference: https://stedolan.github.io/jq/manual/

    :param program: jq
    :param command:
    :return: return filtered json string

    WARNING: this is still a roughly implementation.
    It requires target machine has a `jq` binary in $PATH.
    """
    cmd = ['jq', program]
    prog = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = prog.communicate(input=command)
    if err:
        raise InvalidJQFilter(err)
    return out
