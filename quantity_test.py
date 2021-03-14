import unittest
from quantity import Quantity


class TestQuantity(unittest.TestCase):

    def test_raises_exception_unit_mismatch(self):
        liquid = Quantity(100, "L")
        solid = Quantity(2, "mg")
        try:
            a = liquid + solid
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_raises_exception_unit_wrong(self):
        try:
            a = Quantity(100, "M")
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, ValueError)

    def test_handle_amount_with_unit(self):
        solid1 = Quantity("100 g", "")
        solid2 = Quantity(2, "mg")
        sum = solid1 + solid2
        self.assertEquals(sum.amount, 100.002)
        self.assertEquals(sum.unit, "g")

    def test_test_addition_grams(self):
        solid1 = Quantity(100, "mg")
        solid2 = Quantity(2, "g")
        sum = solid1 + solid2
        self.assertEquals(sum.amount, 2.1)
        self.assertEquals(sum.unit, "g")

    def test_test_addition_grams_string(self):
        solid1 = Quantity("100", "mg")
        solid2 = Quantity("2", "g")
        sum = solid1 + solid2
        self.assertEquals(sum.amount, 2.1)
        self.assertEquals(sum.unit, "g")

    def test_test_addition_mils(self):
        solid1 = Quantity(100, "mL")
        solid2 = Quantity(2, "L")
        sum = solid1 + solid2
        self.assertEquals(sum.amount, 2100)
        self.assertEquals(sum.unit, "ml")

    def test_test_addition_kilograms_lower(self):
        solid1 = Quantity(1, "Kg")
        self.assertEquals(solid1.amount, 1000)
        self.assertEquals(solid1.unit, "g")

    def test_test_addition_liters_lower(self):
        solid1 = Quantity(2, "L")
        self.assertEquals(solid1.amount, 2000)
        self.assertEquals(solid1.unit, "ml")

    def test_test_addition_grams_lower(self):
        solid1 = Quantity(2, "G")
        self.assertEquals(solid1.amount, 2)
        self.assertEquals(solid1.unit, "g")

    def test_test_addition_milligrams_lower(self):
        solid1 = Quantity(200, "Mg")
        self.assertEquals(solid1.amount, 0.2)
        self.assertEquals(solid1.unit, "g")

    def test_test_addition_milliliters_lower(self):
        solid1 = Quantity(2, "mL")
        self.assertEquals(solid1.amount, 2)
        self.assertEquals(solid1.unit, "ml")

if __name__ == '__main__':
    unittest.main()
