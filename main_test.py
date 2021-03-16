import unittest
from main import is_explosive

class TestCompound(unittest.TestCase):

    def test_is_not_explosive(self):
        self.assertEquals(is_explosive(["H281", "H290"]), "no" )

    def test_is_explosive(self):
        self.assertEquals(is_explosive(["H281", "H290", "H225"]), "yes")

    def test_is_not_explosive_when_empty(self):
        self.assertEquals(is_explosive([]), "no")
