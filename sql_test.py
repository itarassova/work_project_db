import unittest
from sql import Database
from compound import Compound
from hazard import Hazard, HazardTypes

cache = None

def setUpModule():
    cache = Database(':memory:')

class CacheTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache = Database(':memory:')

    
    
    def test_get_hazards_from_compound(self):
        test_compound = Compound('141-97-9', 'Ethyl acetoacetate')
        result_hazards = self.cache.get_hazards_from_compound(test_compound)
        self.assertEqual(result_hazards, None)

    def test_insert_compound_hazard(self):
        test_compound = Compound('141-97-9', 'Ethyl acetoacetate')
        test_compound_hazards = [Hazard('H315', '(14.9%): Causes skin irritation '), Hazard('H318', '(14.9%): Causes serious eye damage ')]
        self.cache.insert_compound_hazard(test_compound, test_compound_hazards)
        result = self.cache.get_hazards_from_compound(test_compound)
        print(result)
        self.assertSetEqual(set(result), {Hazard('H315', '(14.9%): Causes skin irritation '), Hazard('H318', '(14.9%): Causes serious eye damage ')})

    def test_insert_duplicate_compound(self):
        test_compound = Compound('103-63-9', '(2-Bromoethyl)benzene')
        test_compound_hazards = [Hazard('H315', '(14.9%): Causes skin irritation '), Hazard('H318', '(14.9%): Causes serious eye damage ')]
        self.cache.insert_compound_hazard(test_compound, test_compound_hazards)
        self.cache.insert_compound_hazard(test_compound, test_compound_hazards)
        result = self.cache.get_reagent_id_from_db(test_compound)
        self.assertEqual(result, 1)
       
       
        
        
    
