# -*- coding: utf-8 -*-

import pytest

@pytest.mark.parametrize('data, env, result', [
    (1, {}, 1),
    ('1', {}, '1'),
    ("{{$TOKEN}}", {}, ''),
    ("{{$TOKEN}}", {"TOKEN": "secretkey"}, 'secretkey'),
    ("{{ $TOKEN }}", {"TOKEN": "secretkey"}, 'secretkey'),
    ("Bearer {{ $TOKEN }}", {"TOKEN": "secretkey"}, 'Bearer secretkey'),
    (['{{$K}}'], {'K': 'V'}, ['V']),
    ({'{{$K}}': 'K'}, {'K': 'V'}, {'V': 'K'}),
])
def test_formatenv(data, env, result):
    from pia.utils import formatenv
    assert formatenv(data, env) == result
