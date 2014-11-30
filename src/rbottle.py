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

    Raises:
        HTTPError: 400 in case the data was malformed.
    """
    raw_data = request.body.read()

    try:
        return json.loads(raw_data)
    except ValueError as e:
        raise HTTPError(400, e.message)


def handle_type_error(fn):
    """
    Convert ``TypeError`` to ``bottle.HTTPError`` with ``400`` code and message
    about wrong parameters.

    Raises:
        HTTPError: 400 in case too many/too little function parameters were \
                   given.
    """
    @wraps(fn)
    def handle_type_error_wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except TypeError as e:
            msg = e.message
            if fn.__name__ in msg and \
               ("got an unexpected" in msg or "takes exactly" in msg):
                raise HTTPError(400, msg)

            raise  # This will cause 500: Internal server error

    return handle_type_error_wrapper


def json_to_params(fn=None, return_json=True):
    """
    Convert JSON in the body of the request to the parameters for the wrapped
    function.

    If the JSON is list, add it to ``*args``.

    If dict, add it to ``**kwargs`` in non-rewrite mode (no key in ``**kwargs``
    will be overwritten).

    If single value, add it to ``*args``.

    Args:
        return_json (bool, default True): Should the decorator automatically
                    convert returned value to JSON?
    """
    def json_to_params_decorator(fn):
        @wraps(fn)
        @handle_type_error
        def json_to_params_wrapper(*args, **kwargs):
            data = decode_json_body()

            if type(data) in [tuple, list]:
                args = list(args) + data
            elif type(data) == dict:
                # transport only items that are not already in kwargs
                allowed_keys = set(data.keys()) - set(kwargs.keys())
                for key in allowed_keys:
                    kwargs[key] = data[key]
            elif type(data) in [bool, int, float, long, str, unicode]:
                args = list(args)
                args.append(data)

            if not return_json:
                return fn(*args, **kwargs)

            return json.dumps(
                fn(*args, **kwargs)
            )

        return json_to_params_wrapper

    if fn:  # python decorator with optional parameters bukkake
        return json_to_params_decorator(fn)

    return json_to_params_decorator


def json_to_data(fn=None, return_json=True):
    """
    Decode JSON from the request and add it as ``data`` parameter for wrapped
    function.

    Args:
        return_json (bool, default True): Should the decorator automatically
                    convert returned value to JSON?
    """
    def json_to_data_decorator(fn):
        @wraps(fn)
        @handle_type_error
        def get_data_wrapper(*args, **kwargs):
            kwargs["data"] = decode_json_body()

            if not return_json:
                return fn(*args, **kwargs)

            return json.dumps(
                fn(*args, **kwargs)
            )

        return get_data_wrapper

    if fn:  # python decorator with optional parameters bukkake
        return json_to_data_decorator(fn)

    return json_to_data_decorator


def form_to_params(fn=None, return_json=True):
    """
    Convert bottle forms request to parameters for the wrapped function.

    Args:
        return_json (bool, default True): Should the decorator automatically
                    convert returned value to JSON?
    """
    def forms_to_params_decorator(fn):
        @wraps(fn)
        @handle_type_error
        def forms_to_params_wrapper(*args, **kwargs):
            kwargs.update(
                dict(request.forms)
            )

            if not return_json:
                return fn(*args, **kwargs)

            return json.dumps(
                fn(*args, **kwargs)
            )

        return forms_to_params_wrapper

    if fn:  # python decorator with optional parameters bukkake
        return forms_to_params_decorator(fn)

    return forms_to_params_decorator
