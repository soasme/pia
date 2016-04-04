# -*- coding: utf-8 -*-
"""
pia.core
~~~~~~~~~~~

Implement core objects for pia.
"""

from celery import Celery

#: celery is the worker runner
celery = Celery('pia')
