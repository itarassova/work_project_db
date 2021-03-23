import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time
import logging as log
import sqlite3
from main import get_cid
from main import get_hazards
from compound import Compound
from hazard import Hazard

conn = sqlite3.connect('Charnwood_inventory_back-up.db')
cursor = conn.cursor()

def insert_compound(compound):

    cursor.execute(''' INSERT INTO REAGENTS_CAS (cas, name) VALUES (?, ?) ''', (compound.cas, compound.name))
    conn.commit()

def insert_hazard(hazard):
    cursor.execute(''' INSERT INTO HAZARDS (hazard_type, hazard_code, hazard_description) VALUES (?, ?, ?), () ''', (hazard.get_type(), hazard.code, hazard.warning_line))
    conn.commit()



