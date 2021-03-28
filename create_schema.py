import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time
import logging as log
import sqlite3
#from main import get_cid
#from main import get_hazards


conn = sqlite3.connect('Charnwood_inventory_back-up.db')
cursor = conn.cursor()
cursor.executescript('''CREATE TABLE REAGENTS_CAS (
            [reagent_id] INTEGER PRIMARY KEY,
            [cas] text, 
            [name] text
            );


                        CREATE TABLE HAZARDS (
            [hazard_id] INTEGER PRIMARY KEY,
            [hazard_type] text, [hazard_code] text,  
            [hazard_description] text 
            );

                        CREATE TABLE REAGENTS_HAZARDS (
            [reagent_id] INTEGER PRIMARY KEY,
            [hazard_id] integer
            );
            ''')

conn.commit()

