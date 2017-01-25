Changelog
=========

0.4.2
-----
    - Fixed #8 - deprecation warning when accessing the Exception.message property.

0.4.1
-----
    - Merged #5 to fix ``docs/__init__.py``, which didn't work at Python 3.
    - Rewritten ``docs/__init__.py``, when the merge for Python 3 broken Python 2 support.

0.4.0
-----
    - Added ``pretty_dump()`` decorator.

0.3.2
-----
    - Fixed bug in @wraps, caused by some strange python behaviour.

0.3.1
-----
    - Fixed bug in documentation.

0.3.0
-----
    - As suggested in #3 - project renamed from ``rbottle`` to ``bottle-rest``.

0.2.0
-----
    - Fixed some bugs, added optional return_json=True parameters.
    - Added pretty print for returned JSON.

0.1.0
-----
    - Project created.
