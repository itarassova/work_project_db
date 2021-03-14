#!/bin/python3

import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time
import logging as log
from quantity import Quantity


start = time.time()

wb = load_workbook(filename='inventoryexport_trial.xlsx')
ws = wb.active

export_workbook = Workbook()
export_worksheet = export_workbook.active

issues_workbook = Workbook()
issues_worksheet = issues_workbook.active

def get_room_from_location(location):
    location_split = location.split('>')[1]
    substring = ' - '
    if substring in location_split:
        room = location_split.split('-')[1]
    else:
        room = location_split.split()[1]
    return room


def get_hazards(cas):
    cid_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(cas)
    cid_resp = requests.get(url=cid_url)
    cid = cid_resp.json()["IdentifierList"]["CID"][0]
    log.info(cid)
    msds_url = "https://pubchem.ncbi.nlm.nih.gov/compound/{}#datasheet=LCSS".format(cas)
    compound_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON".format(cid)
    resp = requests.get(url=compound_url)
    data = resp.json()
    filter_expression = parser.parse('$.Record.Section[?(@.TOCHeading=="Safety and Hazards")].Section[0].Section[0].Information[2].Value.StringWithMarkup[*].String')
    health_warning_lines = []
    physical_warning_lines = []
    environmental_warning_lines = []
    other_hazards = []
    for warning_line in filter_expression.find(data):
        log.info(warning_line.value)        
        if warning_line.value[1] == '2':
            physical_warning_lines.append(warning_line.value)
        elif warning_line.value[1] == '3':
            health_warning_lines.append(warning_line.value)
        elif warning_line.value[1] == '4':
            environmental_warning_lines.append(warning_line.value)
        else:
            other_hazards.append(warning_line.value)
    return physical_warning_lines, health_warning_lines, environmental_warning_lines, other_hazards, msds_url

substances = {}

for row in ws.iter_rows(min_row = 2):
    try:
        name = row[0].value        
        cas = row[1].value
        if not cas:
            raise ValueError("No CAS present")
        room_location = get_room_from_location(row[7].value)
        amount = Quantity(row[2].value, row[3].value)
        
        locations = substances.get(cas, {})
        amount_in_location = locations.get(room_location)
        if not amount_in_location:
            locations[room_location] = amount
        else:
            amount_in_location += amount
        substances[cas] = locations
        
    except Exception as e:
        log.error(e, exc_info=True)
        print(str(cas) + ' didn\'t work')
        issues_worksheet[row] = ws[row]

# substances = {"1234-56-78": {"Room 1": "15 ml", "Room 2": "30 ml"}, "9876-5-32" {"Room 1": "15 g", "Room 2": "30 g"}}

row_number = 1
for cas in substances:
    locations = substances[cas]
    physical_warning_lines, health_warning_lines, environmental_warning_lines, other_hazards, msds_url = get_hazards(cas)
    physical_hazards = '\n'.join(physical_warning_lines)
    health_hazards = '\n'.join(health_warning_lines)
    environmental_hazards = '\n'.join(environmental_warning_lines)
    other_hazards = '\n'.join(other_hazards)
    for location in locations:
        row_number += 1
        amount = locations[location]
        #export_worksheet['A'+ str(row)] = str(name)
        export_worksheet['B'+ str(row_number)] = str(cas)
        export_worksheet['C'+ str(row_number)] = str(physical_hazards)
        export_worksheet['E'+ str(row_number)] = str(health_hazards)
        export_worksheet['F'+ str(row_number)] = str(environmental_hazards)
        export_worksheet['G'+ str(row_number)] = str(other_hazards)
        export_worksheet['H'+ str(row_number)] = str(msds_url)
        export_worksheet['I'+ str(row_number)] = str(room_location)
        
    

    


export_workbook.save(filename="test_output.xlsx")
end = time.time()
print(end-start)
