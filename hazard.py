#from main import get_cid
#from main import get_hazards
from enum import Enum, auto
import requests
import logging as log
import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser

        

class HazardTypes(Enum):
    PHYSICAL = auto() #auto()
    HEALTH = auto()
    ENVIRONMENTAL = auto()
    OTHER = auto()


class Hazard:
    def __init__(self, code, warning_line):
        self.code = code
        self.warning_line = warning_line
        

    def get_type(self):
        if self.code[1] == '2':
            return HazardTypes.PHYSICAL
        if self.code[1] == '3':
            return HazardTypes.HEALTH
        if self.code[1] == '4':
            return HazardTypes.ENVIRONMENTAL
        return HazardTypes.OTHER

    def is_explosive(self) -> bool:
        non_explosive_codes = ['h290', 'h281']
        if self.get_type() == HazardTypes.PHYSICAL:
            if self.code.casefold() not in non_explosive_codes:
                return True
        return False
    
    
          
