# -*- coding: utf-8 -*-
"""
Pia utils
~~~~~~~~~~~~~~~

Utility functions for pia.
"""

import re

ENV_PLACEHODLER = re.compile(r'{{\s?\$(\w+)\s?}}')

def formatenv(data, env):
    """
    Format data with given env.

    :param data: a string/integer/float/boolean/list/dict object.
    :param env: a dictionary.
    :return: return formatted data.

    `formatenv` will try to format strings contained env placeholder `{{ $ENV_KEY }}`.

    If `ENV_KEY` does not exist in env, then this key will be formatted to empty string.
    """
    if isinstance(data, list):
        return [formatenv(datum, env) for datum in data]
    elif isinstance(data, dict):
        return {
            formatenv(key, env): formatenv(value, env)
            for key, value in data.items()
        }
    elif isinstance(data, str):
        return ENV_PLACEHODLER.sub(
            lambda match: env.get(match.group(1), ''),
            data
        )
    else:
        return data
