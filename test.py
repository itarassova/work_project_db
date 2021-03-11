#!/bin/python3

import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time

start = time.time()

wb = load_workbook(filename='inventoryexport_trial.xlsx')
ws = wb.active

export_workbook = Workbook()
export_worksheet = export_workbook.active

row = 2

#list_cas = []

#for col in ws['B']:
    #list_cas.append(col.value)

#substance_name_list = []

#for col in ws['A']:
    #substance_name_list.append(col.value)

#row_substance = 2
#for substance in substance_name_list:
    #export_worksheet['G'+ str(row_substance)] = str(substance)
    #row_substance+=1

#location_list = []

#for col in ws['H']:
    #location_list.append(col.value)

#row_location = 2
#for location in location_list:
    #room_location = location.split('>')[1]
    #print(room_location)
    #xport_worksheet['H'+ str(row_location)] = str(room_location)
    #row_location+=1





for cell in ws['B']:
    try:
        cas = cell.value
        cid_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(cas)
        cid_resp = requests.get(url=cid_url)
        cid = cid_resp.json()["IdentifierList"]["CID"][0]
        print(cid)
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
            print(warning_line.value)        
            if warning_line.value[1] == '2':
                physical_warning_lines.append(warning_line.value)
            elif warning_line.value[1] == '3':
                health_warning_lines.append(warning_line.value)
            elif warning_line.value[1] == '4':
                environmental_warning_lines.append(warning_line.value)
            else:
                other_hazards.append(warning_line.value)
            

        physical_hazards = '\n'.join(physical_warning_lines)
        health_hazards = '\n'.join(health_warning_lines)
        environmental_hazards = '\n'.join(environmental_warning_lines)
        other_hazards = '\n'.join(other_hazards)

        export_worksheet['A'+ str(row)] = str(cas)
        export_worksheet['B'+ str(row)] = str(physical_hazards)
        export_worksheet['C'+ str(row)] = str(health_hazards)
        export_worksheet['D'+ str(row)] = str(environmental_hazards)
        export_worksheet['E'+ str(row)] = str(other_hazards)
        export_worksheet['F'+ str(row)] = str(msds_url)
        export_worksheet['G'+ str(row)] = str(ws['A'+str(row-1)].value)
        export_worksheet['H'+ str(row)] = str(ws['H'+str(row-1)].value).split('>')[1]
        
        

        

        






        
        row+=1

    except:
        print(str(cas) + ' didn\'t work')

export_workbook.save(filename="test_output.xlsx")
end = time.time()
print(end-start)
