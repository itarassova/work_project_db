import unittest
from hazard import Hazard, HazardTypes

def test_equality(self):
    hazardOne = Hazard("123", "Test")
    hazardTwo = Hazard("123", "Test")
    self.assertEqual(hazardOne, hazardTwo)
