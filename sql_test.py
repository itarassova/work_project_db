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

    def test_insert_compound(self):
        test_compound = Compound('103-63-9', '(2-Bromoethyl)benzene')
        self.cache.insert_compound(test_compound)
        result = self.cache.get_compound_by_cas(test_compound)
        self.assertEqual(len(result), 1)
        query_tuple = result[0]
        self.assertEqual((query_tuple[0], query_tuple[1]), (test_compound.cas, test_compound.name))


    def test_insert_duplicate_compound(self):
        test_compound = Compound('103-63-9', '(2-Bromoethyl)benzene')
        self.cache.insert_compound(test_compound)
        self.cache.insert_compound(test_compound)
        result = self.cache.get_compound_by_cas(test_compound)
        self.assertEqual(len(result), 1)
        query_tuple = result[0]
        self.assertEqual((query_tuple[0], query_tuple[1]), (test_compound.cas, test_compound.name))

    def test_insert_hazard(self):
        test_hazard = Hazard('H315', 'Causes skin irritation')
        test_compound = Compound('99646-28-3', '( R )-Tol-BINAP')
        self.cache.insert_hazard(test_hazard, test_compound)
        result = self.cache.get_hazard_from_db(test_hazard)
        self.assertEqual(len(result), 1)
        query_tuple = result[0]
        self.assertEqual((query_tuple[0], query_tuple[1], query_tuple[2]), (test_hazard.code, test_hazard.warning_line, test_hazard.get_type()))
        
    
