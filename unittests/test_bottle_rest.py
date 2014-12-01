#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
from StringIO import StringIO

import pytest

sys.path = ['src/bottle_rest'] + sys.path
import bottle_rest
from bottle_rest import HTTPError


# Functions & classes =========================================================
class MockRequest:
    def __init__(self, json):
        self.body = StringIO(json)
        self.forms = {}


def test_decode_json_body():
    bottle_rest.request = MockRequest('{"hello": "there"}')

    assert bottle_rest.decode_json_body() == {"hello": "there"}

    with pytest.raises(HTTPError):
        bottle_rest.request = MockRequest('{')
        bottle_rest.decode_json_body()


def test_encode_json_body():
    assert bottle_rest.encode_json_body({"one": 1}) == '''{
    "one": 1
}'''


def test_handle_type_error():
    @bottle_rest.handle_type_error
    def too_much_parameters(one):
        pass

    with pytest.raises(HTTPError):
        too_much_parameters("one", "two")

    @bottle_rest.handle_type_error
    def too_few_parameters(one, two, three):
        pass

    with pytest.raises(HTTPError):
        too_few_parameters("one")

    @bottle_rest.handle_type_error
    def exactly_right_ammount_of_parameters(one):
        pass

    assert exactly_right_ammount_of_parameters("one") is None


# json_to_params tests ========================================================
def test_json_to_params():
    bottle_rest.request = MockRequest('{"param": 2}')

    @bottle_rest.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"  # serialized to json


def test_json_to_params_no_json_parameter():
    bottle_rest.request = MockRequest('{"param": 2}')

    @bottle_rest.json_to_params(return_json=False)
    def json_to_params_test_no_json(param):
        return param * 2

    assert json_to_params_test_no_json() == 4


def test_json_to_params_list():
    bottle_rest.request = MockRequest('[2]')  # different parameter is used

    @bottle_rest.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"


def test_json_to_params_value():
    bottle_rest.request = MockRequest('2')  # different parameter is used

    @bottle_rest.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"


def test_json_to_params_bad_keyword():
    bottle_rest.request = MockRequest('{"nope": 1}')

    @bottle_rest.json_to_params
    def json_to_params_test(param):
        return param * 2

    with pytest.raises(HTTPError):
        json_to_params_test()


# json_to_data tests ==========================================================
def test_json_to_data():
    bottle_rest.request = MockRequest('2')

    @bottle_rest.json_to_data
    def json_to_data_test(data):
        return data * 2

    assert json_to_data_test() == "4"


def test_json_to_data_no_json_parameter():
    bottle_rest.request = MockRequest('2')

    @bottle_rest.json_to_data(return_json=False)  # don't convert result to JSON
    def json_to_data_test(data):
        return data * 2

    assert json_to_data_test() == 4


def test_json_to_data_error_too_few():
    bottle_rest.request = MockRequest('2')

    @bottle_rest.json_to_data
    def json_to_data_test():
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


def test_json_to_data_error_too_many():
    bottle_rest.request = MockRequest('2')

    @bottle_rest.json_to_data
    def json_to_data_test(one, two):
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


# form_to_params tests ========================================================
def test_form_to_params():
    bottle_rest.request = MockRequest('""')
    bottle_rest.request.forms = {"param": 2}

    @bottle_rest.form_to_params
    def form_to_params_test(param):
        return param * 2

    assert form_to_params_test() == "4"


def test_form_to_params_no_json_parameter():
    bottle_rest.request = MockRequest('""')
    bottle_rest.request.forms = {"param": 2}

    # don't convert result to JSON
    @bottle_rest.form_to_params(return_json=False)
    def form_to_params_test(param):
        return param * 2

    assert form_to_params_test() == 4
