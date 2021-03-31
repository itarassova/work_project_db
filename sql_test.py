import unittest
from sql import Cache
from compound import Compound
from hazard import Hazard, HazardTypes, get_hazards,get_cid
import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser


cache = None

def setUpModule():
    cache = Cache(':memory:')

class CacheTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cache = Cache(':memory:')

    #def test_insert_compound(self):
        #test_compound = Compound('103-63-9', '(2-Bromoethyl)benzene')
        #self.cache.insert_compound_hazard(test_compound)
        #result = self.cache.get_compound_from_db(test_compound)
        #self.assertEqual(len(result), 1)
        #query_tuple = result[0]
        #self.assertEqual((query_tuple[0], query_tuple[1]), (test_compound.cas, test_compound.name))


    #def test_insert_duplicate_compound(self):
        #test_compound = Compound('103-63-9', '(2-Bromoethyl)benzene')
        #self.cache.insert_compound_hazard(test_compound)
        #self.cache.insert_compound_hazard(test_compound)
        #result = self.cache.get_compound_from_db(test_compound)
        #self.assertEqual(len(result), 1)
        #query_tuple = result[0]
        #self.assertEqual((query_tuple[0], query_tuple[1]), (test_compound.cas, test_compound.name))

    def test_insert_compound_hazard(self):
        test_compound = Compound('5192-03-0', '5-Aminoindole')
        result_compound = self.cache.get_compound_from_db(test_compound)
        self.assertEqual(result_compound, 1)
        hazard_for_test_compound = Hazard('H315', '(100%): Causes skin irritation ')
        result_hazard = self.cache.get_hazard_from_db(hazard_for_test_compound)
        hazard_output = result_hazard[0]
        self.assertEqual((hazard_output[0], hazard_output[1]), (hazard_for_test_compound.code, hazard_for_test_compound.warning_line))
        
    
