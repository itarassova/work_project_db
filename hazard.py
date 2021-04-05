#from main import get_cid
#from main import get_hazards
from enum import Enum, auto
import requests
import logging as log
import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser

def get_cid(synonum):
    cid_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(
        synonum)
    cid_resp = requests.get(url=cid_url)
    cid = cid_resp.json()["IdentifierList"]["CID"][0]
    log.info(cid)
    return cid
   



def get_hazards(compound):
    try:
        try:
            cid = get_cid(compound.cas)
        except Exception as e:
            cid = get_cid(compound.name)
    except Exception as e:
        no_cid = 'No CID found'
        return no_cid
   
    msds_url = "https://pubchem.ncbi.nlm.nih.gov/compound/{}#datasheet=LCSS".format(
            compound.cas)
    compound_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON".format(
            cid)
    resp = requests.get(url=compound_url)
    data = resp.json()
    filter_expression = parser.parse(
        '$.Record.Section[?(@.TOCHeading=="Safety and Hazards")].Section[0].Section[0].Information[2].Value.StringWithMarkup[*].String')
    hazards = []
    further_information = []
    for warning_expression in filter_expression.find(data):
        log.info(warning_expression.value)
        warning_string = warning_expression.value
        comment_start = warning_string.find("[")
        code = warning_string[0:4]
        warning_line = warning_string[4:comment_start]
        hazard = Hazard(code, warning_line)
        hazards.append(hazard)    
        if comment_start != -1:
            further_information.append(warning_string[comment_start:])
            warning_string = warning_string[:comment_start]
    health_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.HEALTH]
    physical_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.PHYSICAL]
    environmental_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.ENVIRONMENTAL]
    other_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.OTHER]
    return hazards, physical_hazards, health_hazards, environmental_hazards, other_hazards, msds_url, further_information
        

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
    
    
          
