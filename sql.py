import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time
import logging as log
import sqlite3

wb = load_workbook(filename='InventoryExport.xlsx')
ws = wb.active

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
    health_warning_lines = []
    physical_warning_lines = []
    environmental_warning_lines = []
    other_hazards = []
    further_information = []
    for warning_line in filter_expression.find(data):
        log.info(warning_line.value)
        warning_string = warning_line.value
        comment_start = warning_string.find("[")
        if comment_start != -1:
            further_information.append(warning_string[comment_start:])
            warning_string = warning_string[:comment_start]
        if warning_string[1] == '2':
            physical_warning_lines.append(warning_string)
        elif warning_string[1] == '3':
            health_warning_lines.append(warning_string)
        elif warning_string[1] == '4':
            environmental_warning_lines.append(warning_string)
        else:
            other_hazards.append(warning_string)
    return physical_warning_lines, health_warning_lines, environmental_warning_lines, other_hazards, msds_url, further_information


conn = sqlite3.connect('Charnwood_inventory_back-up.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE REAGENTS CAS
             ([reagent_id] INTEGER PRIMARY KEY,[cas] char''')

cursor.execute('''CREATE TABLE REAGENTS NAME
             ([reagent_id] INTEGER PRIMARY KEY,[name] char''')

cursor.execute('''CREATE TABLE HAZARDS
             ([hazard_id] INTEGER PRIMARY KEY,[hazard_type] char, [hazard_code] char, [hazard_description] varchar(512) ''')

cursor.execute('''CREATE TABLE REAGENTS HAZARDS
             ([reagent_id] INTEGER PRIMARY KEY,[hazard_id] char''')

cursor.execute('''CREATE TABLE REAGENTS LOCATION
             ([reagent_id] INTEGER PRIMARY KEY,[location] char''')

cursor.execute('''CREATE TABLE REAGENTS AMOUNT
             ([reagent_id] INTEGER PRIMARY KEY,[location] char, [mass] decimal (10,2), [volume] decimal (10,2), ''')

