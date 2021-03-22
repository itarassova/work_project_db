from main import get_cid
from main import get_hazards
from enum import Enum, auto

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
    
    
          
