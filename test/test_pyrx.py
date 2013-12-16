import os
import re
import json
import unittest
import pyrx


class TestSchemas(unittest.TestCase):
    """Some basic sanity checks"""
    def setUp(self):
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
        self.schema = rx.make_schema(schema_src)

    def test_good(self):
        self.assertTrue(self.schema.check({
          "a": "a string",
          "b": 1,
        }))
        self.assertTrue(self.schema.check({
          "a": "a string",
          "b": 1,
          "c": False,
        }))

    def test_bad(self):
        self.assertFalse(self.schema.check({
          "a": ["not just a string"],
          "b": 1,
        }))
        self.assertFalse(self.schema.check({
          "a": "a string",
          "b": "not an int",
        }))
        self.assertFalse(self.schema.check({
          "a": "b is missing",
        }))
        self.assertFalse(self.schema.check({
          "a": "c is not a bool",
          "b": 1,
          "c": None,
        }))



#########    LEGACY TESTS PORT    #########
######### from the original rx.py #########

class LegacyTestsPort(unittest.TestCase):
    """Generate tests from the legacy stuff"""


def check(test_name, method_name, *args):
    if hasattr(LegacyTestsPort, test_name):
        raise NameError('Duplicate test name {}'.format(test_name))
    def test(self):
        getattr(self, method_name)(*args)
    setattr(LegacyTestsPort, test_name, test)


def normalize(entries, test_data):
    if entries == '*':
        entries = { "*": None }

    if type(entries) is type([]):
        new_entries = { }
        for n in entries:
            new_entries[n] = None
        entries = new_entries

    if len(entries) == 1 and '*' in entries:
        value = entries["*"]
        entries = { }
        for k in test_data.keys():
            entries[k] = value

    return entries


# match paths to legacy code
resource = lambda name: json.load(open('test/' + name))


def load_stuff():
    test_data = {}
    test_schemata = {}

    # find data files
    for root, folders, files in os.walk(os.path.join('test', 'spec', 'data')):
        for filename in files:
            leaf_name = filename[:-len('.json')]
            test_data[leaf_name] = {}

            payload = json.load(open(os.path.join(root, filename)))
            if isinstance(payload, list):
                for data_str in payload:
                    test_data[leaf_name][data_str] = json.loads(data_str)
            else:  # should be a dict
                for entry, data_str in payload.items():
                    test_data[leaf_name][entry] = json.loads(data_str)

    # find schemata files
    for root, folders, files in os.walk(os.path.join('test', 'spec', 'schemata')):
        for filename in files:
            leaf_stem = os.path.join(*root.split('/')[2:])
            leaf_name = os.path.join(leaf_stem, filename[:-len('.json')])
            payload = json.load(open(os.path.join(root, filename)))
            test_schemata[leaf_name] = payload

    return test_data, test_schemata


def learn(rx, name, composedtype):
    try:
        rx.learn_type(composedtype['uri'], composedtype['schema'])
    except pyrx.RxError:
        check('test_invalid_composedtype_{}'.format(name), 'assertTrue',
              composedtype.get('invalid', False))
    else:
        if 'invalid' in composedtype:
            check('test_valid_composed_type_{}'.format(name), 'assertFalse',
              composedtype['invalid'])
    return not composedtype.get('invalid', True)


def get_schema(name, schemata):
    rx = pyrx.Factory({"register_core_types": True})

    if 'composedtype' in schemata:
        learnable = learn(rx, name, schemata['composedtype'])
        if not learnable:
            return

    schema = None
    try:
        schema = rx.make_schema(schemata['schema'])
    except pyrx.RxError:
        check('test_invalid_schema_{}'.format(name), 'assertTrue',
              schemata.get('invalid', False))
    else:
        if 'invalid' in schemata:
            check('test_valid_schema_{}'.format(name), 'assertFalse',
                  schema['invalid'])

    return schema


def check_schema(schema, spec, data, name):
    for fail, checks in [(t == 'fail', s) for t, s in spec.items() if t in ('pass', 'fail')]:
        for sourcename, to_test in checks.items():
            normalized = normalize(to_test, data[sourcename])
            for entry in normalized:
                result = schema.check(data[sourcename][entry])
                test_name = 'test_check_schema_{}_{}_{}_{}'.format(name, sourcename, fail, entry)
                check(test_name, 'assertEqual', result, not fail)


rx = pyrx.Factory({"register_core_types": True})
check('test_factory_makes_factory',
      'assertIsInstance', rx, pyrx.Factory)


data, schemata = load_stuff()
for name, spec in schemata.items():
    schema = get_schema(name, spec)
    if schema is not None:
        check_schema(schema, spec, data, name)
