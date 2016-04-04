# -*- coding: utf-8 -*-

import re

ENV_PLACEHODLER = re.compile(r'{{\s?\$(\w+)\s?}}')

def formatenv(data, env):
    """
    >>> formatenv(1, {})
    1
    >>> formatenv('1', {})
    '1'
    >>> formatenv("{{$TOKEN}}", {})
    ''
    >>> formatenv("{{$TOKEN}}", {"TOKEN": "secretkey"})
    'secretkey'
    >>> formatenv("{{ $TOKEN }}", {"TOKEN": "secretkey"})
    'secretkey'
    >>> formatenv("Bearer {{ $TOKEN }}", {"TOKEN": "secretkey"})
    'Bearer secretkey'
    >>> formatenv(['{{$K}}'], {'K': 'V'})
    ['V']
    >>> formatenv({'{{$K}}': 'K'}, {'K': 'V'})
    {'V': 'K'}
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
