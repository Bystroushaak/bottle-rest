rbottle documentation
=====================

Welcome in the rbottle documentation. This package is used to make easier
creating REST applications using `Bottle <http://bottlepy.org>`_ web framework.

API documentation
-----------------
.. toctree::
    :maxdepth: 2

    api/rbottle

Installation
------------
Module is hosted at `PYPI <https://pypi.python.org/pypi/rbottle>`_,
and can be easily installed using
`PIP <http://en.wikipedia.org/wiki/Pip_%28package_manager%29>`_:

::

    sudo pip install rbottle

Testing
-------
This project uses `pytest <http://pytest.org>`_ for testing. You can run
the tests from the root of the package using following command::

    $ py.test

Which will output something like::

    ============================= test session starts ==============================
    platform linux2 -- Python 2.7.6 -- py-1.4.23 -- pytest-2.6.0
    collected 11 items 

    unittests/test_bson_utils.py ..
    unittests/test_rest.py ....
    unittests/test_utils.py .....

    ========================== 11 passed in 0.29 seconds ===========================

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

