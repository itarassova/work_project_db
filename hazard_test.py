import unittest
from hazard import Hazard, HazardTypes

class TestHazard(unittest.TestCase):

    def test_equality(self):
        hazardOne = Hazard("123", "Test")
        hazardTwo = Hazard("123", "Test")
        self.assertEqual(hazardOne, hazardTwo)

    def test_equal_hcode(self):
        hazardOne = Hazard("H319", "[100%] Causes serious eye irritation")
        hazardTwo = Hazard("H319", "[95.85%] Causes serious eye irritation")
        self.assertEqual(hazardOne, hazardTwo)

