from enum import Enum, auto
import requests
import logging as log
import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser


class HazardTypes(Enum):
    PHYSICAL = auto()
    HEALTH = auto()
    ENVIRONMENTAL = auto()
    OTHER = auto()


class Hazard:
    def __init__(self, code, warning_line):
        self.code = code
        self.warning_line = warning_line

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.code == other.code and self.warning_line == other.warning_line

    def __key(self):
        return self.code

    def __str__(self):
        return f'The compound H-code is {self.code} and the warning_line is {self.warning_line}'

    def __repr__(self):
        return f'Hazard(code={self.code}, warning_line={self.warning_line})'

    def __hash__(self):
        return hash(self.__key())    

    def get_type(self) -> HazardTypes:
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

    

    
    
          
