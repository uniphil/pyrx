pyrx
====

[![Build Status](https://travis-ci.org/uniphil/pyrx.png)](https://travis-ci.org/uniphil/pyrx)

Python implementation of the [Rx schema and validation system](http://rx.codesimply.com/)


Forked
------

Forked from the main [rx github repo](https://github.com/rjbs/rx) Nov 25 '13
because the python implementation deserves its own place and testing and stuff.

The copyright line of the license for the rx repository reads:

    The contents of the Rx repository are copyright (C) 2008, Ricardo SIGNES.

The license itself is GPL2: https://github.com/rjbs/rx/blob/master/LICENSE


Requirements
------------

* No external dependencies
* Python2.7 (python3 support coming soon)


Installation
------------

```bash
$ pip install pyrx
```


Usage
-----

```python
import pyrx

rx = pyrx.Factory({"register_core_types": True})

schema_src = {
  "type": "//rec",
  "required": {
    "a": "//str",
    "b": "//int",
  },
  "optional": {
    "c": "//bool",
  },
}

schema = rx.make_schema(schema_src)

schema.check({"a": "a string", "b": 2})  # returns True
schema.check({"a": "a string", "b": "another string"})  # returns False

```


Testing
-------

I didn't bring the tests over from the rx repo. They used `TAP` or something
I'm not familiar with. The tests included here just run through a couple
trivial cases to make sure it doesn't straight-up crash.

So, porting tests will be next up, and then porting to python3.

And then built-in support for files, both json and yaml. Maybe...
