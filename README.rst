===============================
bamboo
===============================

.. image:: https://img.shields.io/pypi/v/bamboo.svg
        :target: https://pypi.python.org/pypi/bamboo

.. image:: https://img.shields.io/travis/soasme/bamboo.svg
        :target: https://travis-ci.org/soasme/bamboo

.. image:: https://readthedocs.org/projects/bamboo/badge/?version=latest
        :target: https://readthedocs.org/projects/bamboo/?badge=latest
        :alt: Documentation Status


Not written yet.

* Free software: ISC license
* Documentation: https://bamboo.readthedocs.org.

Quick Start
-----------

Example::

    $ cat programs/soasme/weather.yml
    pipe:
    - method: get
      url: https://query.yahooapis.com/v1/public/yql
      params:
        format: json
        q: 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="beijing")'
    - method: post
      url: http://127.0.0.1:8000/builtin/jq
      params:
        program: '.query.results.channel|{title:.description,wind:.wind.speed|tonumber|(./3.60)|tostring,forcast:.item.forecast[0].text}'

    $ curl -H"content-type: application/json" -d '{"message":"hello world"}' -X POST "http://127.0.0.1:8000/soasme/weather?city=beijing"
    {"title": "Yahoo! Weather for Beijing, Beijing, CN", "wind": "3.0555555555555554", "forcast": "Sunny"}


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
