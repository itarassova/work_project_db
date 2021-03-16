#!/bin/python3

import json
import requests
from jsonpath_ng import jsonpath, parse
from openpyxl import Workbook, load_workbook


cas = '99646-28-3'
cid_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON".format(cas)
cid_resp = requests.get(url=cid_url)
cid = cid_resp.json()["IdentifierList"]["CID"][0]
print(cid)
compound_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON".format(cid)
resp = requests.get(url=compound_url)
data = resp.json()
filter_expression = parse('$.Record.Section[9].Section[0].Section[0].Information[2].Value.StringWithMarkup[*].String')
for warning_line in filter_expression.find(data):
    print(warning_line.value)
