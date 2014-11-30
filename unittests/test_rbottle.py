#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import sys
from StringIO import StringIO
sys.path.append('src/')

import pytest
from bottle import HTTPError

import rbottle



# Functions & classes =========================================================
class MockRequest:
    def __init__(self, json):
        self.body = StringIO(json)
        self.forms = {}


def test_decode_json_body():
    rbottle.request = MockRequest('{"hello": "there"}')

    assert rbottle.decode_json_body() == {"hello": "there"}

    with pytest.raises(HTTPError):
        rbottle.request = MockRequest('{')
        rbottle.decode_json_body()


def test_handle_type_error():
    @rbottle.handle_type_error
    def too_much_parameters(one):
        pass

    with pytest.raises(HTTPError):
        too_much_parameters("one", "two")

    @rbottle.handle_type_error
    def too_few_parameters(one, two, three):
        pass

    with pytest.raises(HTTPError):
        too_few_parameters("one")

    @rbottle.handle_type_error
    def exactly_right_ammount_of_parameters(one):
        pass

    assert exactly_right_ammount_of_parameters("one") is None


# json_to_params tests ========================================================
def test_json_to_params():
    rbottle.request = MockRequest('{"param": 2}')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"  # serialized to json


def test_json_to_params_no_json_parameter():
    rbottle.request = MockRequest('{"param": 2}')

    @rbottle.json_to_params(return_json=False)
    def json_to_params_test_no_json(param):
        return param * 2

    assert json_to_params_test_no_json() == 4


def test_json_to_params_list():
    rbottle.request = MockRequest('[2]')  # different parameter is used

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"


def test_json_to_params_value():
    rbottle.request = MockRequest('2')  # different parameter is used

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    assert json_to_params_test() == "4"


def test_json_to_params_bad_keyword():
    rbottle.request = MockRequest('{"nope": 1}')

    @rbottle.json_to_params
    def json_to_params_test(param):
        return param * 2

    with pytest.raises(HTTPError):
        json_to_params_test()


# json_to_data tests ==========================================================
def test_json_to_data():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test(data):
        return data * 2

    assert json_to_data_test() == "4"


def test_json_to_data_no_json_parameter():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data(return_json=False)  # don't convert result to JSON
    def json_to_data_test(data):
        return data * 2

    assert json_to_data_test() == 4


def test_json_to_data_error_too_few():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test():
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


def test_json_to_data_error_too_many():
    rbottle.request = MockRequest('2')

    @rbottle.json_to_data
    def json_to_data_test(one, two):
        pass

    with pytest.raises(HTTPError):
        json_to_data_test()


# form_to_params tests ========================================================
def test_form_to_params():
    rbottle.request = MockRequest('""')
    rbottle.request.forms = {"param": 2}

    @rbottle.form_to_params
    def form_to_params_test(param):
        return param * 2

    assert form_to_params_test() == "4"


def test_form_to_params_no_json_parameter():
    rbottle.request = MockRequest('""')
    rbottle.request.forms = {"param": 2}

    @rbottle.form_to_params(return_json=False)  # don't convert result to JSON
    def form_to_params_test(param):
        return param * 2

    assert form_to_params_test() == 4
