#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from setuptools import setup, find_packages


# Functions & classes =========================================================
setup(
    name='rbottle',
    version='0.1.1',
    description="Decorators to make REST easier in Bottle.",
    long_description=open("README.rst").read(),
    url='https://github.com/Bystroushaak/rbottle',

    author='Bystroushaak',
    author_email='bystrousak@kitakitsune.org',

    classifiers=[
        "Framework :: Bottle",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
    ],
    license='MIT',

    packages=find_packages(".", exclude=['ez_setup']),
    package_dir={'': 'src'},

    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'setuptools',
        "bottle",
        "sphinxcontrib-napoleon>=0.2.5"  # napoleon docstrings
    ],
)
