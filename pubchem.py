import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from compound import Compound
from hazard import Hazard, HazardTypes
import logging as log


def get_cid(synonum):
    cid_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(
        synonum)
    cid_resp = requests.get(url=cid_url)
    cid = cid_resp.json()["IdentifierList"]["CID"][0]
    log.info(cid)
    return cid


def get_hazards(compound):
    try:
        cid = get_cid(compound.cas)
    except Exception as e:
        cid = get_cid(compound.name)
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
        hazard.append(hazards)    
        if comment_start != -1:
            further_information.append(warning_string[comment_start:])
            warning_string = warning_string[:comment_start]
        return hazards, msds_url
    
def some_method(hazards):
    health_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.HEALTH]
    physical_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.PHYSICAL]
    environmental_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.ENVIRONMENTAL]
    other_hazards = [hazard for hazard in hazards if hazard.get_type() == HazardTypes.OTHER]
    return physical_hazards, health_hazards, environmental_hazards, other_hazards

