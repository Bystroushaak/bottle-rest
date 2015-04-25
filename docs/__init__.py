#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7, 3.4
#


def allSame(s):
    return not any(filter(lambda x: x != s[0], s))


def hasDigit(s):
    return any(char.isdigit() for char in s)


def getVersion(data):
    """
    Parse version from changelog written in RST format.
    """
    data = data.splitlines()
    return next((
        v
        for v, u in zip(data, data[1:])  # v = version, u = underline
        if len(v) == len(u) and allSame(u) and hasDigit(v) and "." in v
    ))
