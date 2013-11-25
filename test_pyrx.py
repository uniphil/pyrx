import unittest
import pyrx


class TestSchemas(unittest.TestCase):

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