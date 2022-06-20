#! /usr/bin/env python3
from setuptools import setup, find_packages

from docs import getVersion


changelog = open("CHANGES.rst").read()
long_description = "\n\n".join([open("README.rst").read(), changelog])


setup(
    name="bottle-rest",
    version=getVersion(changelog),
    description="Decorators to make REST easier in Bottle.",
    long_description=long_description,
    url="https://github.com/Bystroushaak/rbottle",
    author="Bystroushaak",
    author_email="bystrousak@kitakitsune.org",
    classifiers=[
        "Framework :: Bottle",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        "setuptools",
        "bottle",
    ],
    extras_require={
        "test": ["pytest"],
        "docs": [
            "sphinx",
            "sphinxcontrib-napoleon",
        ],
    },
)
