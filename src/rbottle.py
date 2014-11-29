#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import json
from functools import wraps

from bottle import request, HTTPError


# Functions & classes =========================================================
def decode_json_body():
    """
    Decode ``bottle.request.body`` to JSON.

    Returns:
        obj: Structure decoded by ``json.loads()``.
    """
    raw_data = request.body.readlines()

    if type(raw_data) in [list, tuple]:
        raw_data = "".join(raw_data)

    return json.loads(raw_data)


def handle_type_error(fn):
    """
    Convert ``TypeError`` to ``bottle.HTTPError`` with ``400`` code and message
    about wrong parameters.
    """
    @wraps(fn)
    def handle_type_error_wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except TypeError as e:
            if "got an unexpected" in e.message:
                raise HTTPError(400, e.message)

            raise

    return handle_type_error_wrapper


def json_to_params(fn):
    """
    Convert JSON in the body of the request to the parameters for the wrapped
    function.

    If the JSON is list, add it to ``*args``.

    If dict, add it to ``**kwargs`` in non-rewrite mode (no key in ``**kwargs``
    will be overwritten).

    If single value, add it to ``*args``.
    """
    @wraps(fn)
    @handle_type_error
    def dejson_wrapper(*args, **kwargs):
        data = decode_json_body()

        if type(data) in [tuple, list]:
            args += data
        elif type(data) == dict:
            # transport only items that are not already in kwargs
            allowed_keys = set(data.keys()) - set(kwargs.keys())
            for key in allowed_keys:
                kwargs[key] = data[key]
        elif type(data) in [bool, int, float, long, str, unicode]:
            args += [data]

        return json.dumps(
            fn(*args, **kwargs)
        )

    return dejson_wrapper


def json_to_data(fn):
    """
    Decode JSON from the request and add it as ``data`` parameter for wrapped
    function.
    """
    @wraps(fn)
    @handle_type_error
    def get_data_wrapper(*args, **kwargs):
        kwargs["data"] = decode_json_body()

        return json.dumps(
            fn(*args, **kwargs)
        )

    return get_data_wrapper


def form_to_params(fn):
    """
    Convert bottle forms request to parameters for the wrapped function.
    """
    @wraps(fn)
    @handle_type_error
    def param_wrapper(*args, **kwargs):
        kwargs.update(
            dict(request.forms)
        )

        return fn(*args, **kwargs)

    return param_wrapper
