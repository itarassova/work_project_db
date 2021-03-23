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


wb = load_workbook(filename='InventoryExport.xlsx')
ws = wb.active

conn = sqlite3.connect('Charnwood_inventory_back-up.db')
cursor = conn.cursor()
cursor.executescript('''CREATE TABLE REAGENTS_CAS (
            [reagent_id] INTEGER PRIMARY KEY,
            [cas] char, 
            [name] char
            );


                        CREATE TABLE HAZARDS (
            [hazard_id] INTEGER PRIMARY KEY,
            [hazard_type] char, [hazard_code] char, 
            [hazard_description] varchar(512)
            );

                        CREATE TABLE REAGENTS_HAZARDS (
            [reagent_id] INTEGER PRIMARY KEY,
            [hazard_id] char
            );
            ''')

conn.commit()

