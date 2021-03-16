import unittest
from compound import Compound

class TestCompound(unittest.TestCase):

    def test_compound_creation(self):
        c = Compound("1234565", "Somethingweird")
        self.assertEqual(c.cas, "1234565")

    def test_equality(self):
        x = Compound("1234565", "Somethingweird")
        y = Compound("1234565", "Somethingevenweirder")
        self.assertEqual(x, y)

    def test_dictionary_key_overwrite(self):
        x = Compound("1234565", "Somethingweird")
        y = Compound("1234565", "Somethingevenweirder")
        test_dictionary = {}
        test_dictionary[x] = 1
        test_dictionary[y] = 2
        self.assertEquals(test_dictionary[x], 2)
