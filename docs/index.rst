bottle-rest documentation
=========================

Welcome in the ``bottle-rest`` documentation. This package is used to make easier
creating REST applications using `Bottle <http://bottlepy.org>`_ web framework.

API documentation
-----------------
.. toctree::
    :maxdepth: 2

    api/bottle_rest

What is it
----------
``bottle-rest`` is a collection of decorators, which can transform incoming data
to parameters of your bottle functions/methods and outgoing data to JSON.

REST in bottle
++++++++++++++
Usually, when you try to write simple JSON REST API in bottle, you have to
work with ``request`` object, read the ``request.body`` file, decode the
JSON, do something with the decoded structure and return back some JSON
encoded data.

This is not bad when you have to do it once, but can get pretty annoying when
yout try to build something bigger and have to repeat the steps again and again.

bottle-rest
+++++++++++

``bottle-rest`` gives you three wrappers to make this repetitive work little bit
easier: :func:`.json_to_params`, :func:`.json_to_data` and
:func:`.form_to_params`.

All three of them maps input data to parameters of your function, so instead of
code like*::

    import json
    from bottle import post, request, HTTPError

    @post("/somepath")
    def handler():
        if "somevar" not in body.json:
            raise HTTPError(400, "'somevar' parameter is required!")

        return json.dumps(
            database[body.json[somevar]]
        )

you can use just::

    from bottle import post
    from bottle_rest import json_to_params

    @post("/somepath")
    @json_to_params
    def handler(somevar):
        return database[somevar]

*Edit: Returned dicts are by Bottle automatically converted to JSON, but other types are not. Thats why I am using explicit conversion (also, there is pretty print).

json_to_params
++++++++++++++
As you can probably guess from the name and see in the example, 
:func:`.json_to_params` simply maps the incoming data to parameters for
your function.

There are three possible things you can get from incoming JSON:

- `dictionary`
- `list`
- `basic type`

`Dictionary` is mapped to ``kwargs`` of your functions, in non-rewrite mode
(no existing ``kwargs`` key will be rewritten).

`List` and `basic types` are added at the end of the ``*args`` parameter of
your function.

For the funtion in the example, you can send::

    {
        "somevar": "somevalue"
    }

or::

    ["somevalue"]

or::

    "somevalue"

with same results.

All returned data from wrapped function will be automatically converted to the
JSON, unless the ``return_json=False`` parameter is specified.

json_to_data
++++++++++++
:func:`.json_to_params` works almost identically as previous function, except
that it puts all the decoded data into ``data`` parameter of your function,
so better make sure, that you have it defined.

This can be useful for bigger sets of the data, which could be impractical to
put into parameters.

All returned data from wrapped function will be automatically converted to the
JSON, unless the ``return_json=False`` parameter is specified.

form_to_params
++++++++++++++
Finally :func:`.form_to_params` works same way as :func:`.json_to_params`,
but it doesn't decodes the input data, but data sent as ``GET`` or ``POST``
request parameters.

Note: In PHP, you would get this using the infamous ``$_GET`` and ``$_POST``
variables.

All returned data from wrapped function will be automatically converted to the
JSON, unless the ``return_json=False`` parameter is specified.

Installation
------------
Module is hosted at `PYPI <https://pypi.python.org/pypi/bottle-rest>`_,
and can be easily installed using
`PIP <http://en.wikipedia.org/wiki/Pip_%28package_manager%29>`_:

::

    sudo pip install bottle-rest

Testing
-------
This project uses `pytest <http://pytest.org>`_ for testing. You can run
the tests from the root of the package using following command::

    $ py.test unittests/

Which will output something like::

 ============================= test session starts ==============================
 platform linux2 -- Python 2.7.6 -- py-1.4.23 -- pytest-2.6.0
 collected 13 items 
 
 unittests/test_bottle_rest.py .............
 
 ========================== 13 passed in 0.09 seconds ===========================


Source code
-----------
This project is released as opensource (MIT) and source codes can be found at
GitHub:

- https://github.com/Bystroushaak/bottle-rest


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
