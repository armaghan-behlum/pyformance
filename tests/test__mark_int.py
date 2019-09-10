from unittest import TestCase
from pyformance import MarkInt
from pprint import pformat


class MarkIntTest(TestCase):
    def test_str_returns_correct_value(self):
        instance = MarkInt(1)

        self.assertEqual("1", str(instance))

    def test_value_is_floored(self):
        # flooring specifically is checked since that's what you expect python to do on int()
        instance = MarkInt(1.5)

        self.assertEqual("1", str(instance))

    def test_repr_returns_descriptive_string(self):
        instance = MarkInt(1)

        # pformat returns __repr__ without printing
        self.assertEqual("MarkInt(1)", pformat(instance))

    def test_equality_returns_true_when_comparing_different_object_with_same_value(self):
        obja = MarkInt(1)
        objb = MarkInt(1)

        self.assertTrue(obja == objb)

    def test_equality_returns_false_when_comparing_different_object_with_different_value(self):
        obja = MarkInt(1)
        objb = MarkInt(2)

        self.assertFalse(obja == objb)

    def test_equality_returns_false_when_comparing_marked_number_with_anything_else(self):
        obja = MarkInt(1)

        self.assertFalse(obja == 1)
