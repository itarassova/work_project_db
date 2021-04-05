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
from compound import Compound
from hazard import Hazard, HazardTypes, get_hazards, get_cid
from pathlib import Path
import logging as log

log.basicConfig(level=log.INFO)

db_name = 'Charnwood_inventory_back-up_really_large_number.db'

class Cache:
    def __init__(self,db_name):
        db_file = Path(db_name)
        new_db = db_name == ':memory:' or not db_file.is_file()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        if new_db:
            self.__create_schema()
            log.info('Schema created')
        
            

    def __create_schema(self):
        log.info("database schema creation")
        self.cursor.executescript('''CREATE TABLE REAGENTS_CAS (
            [reagent_id] INTEGER PRIMARY KEY,
            [cas] text UNIQUE, 
            [name] text UNIQUE,
            [found_in_pubchem] text
            );


                        CREATE TABLE HAZARDS (
            [hazard_id] INTEGER PRIMARY KEY,
            [hazard_code] text UNIQUE,  
            [hazard_description] text UNIQUE 
            );

                        CREATE TABLE REAGENTS_HAZARDS (
            [reagent_id] INTEGER PRIMARY KEY,
            [hazard_id] integer
            );
            ''')

        self.conn.commit()

    def __get_compound_by_cas(self, compound):
    
        self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE cas = ?''', [compound.cas])
        return self.cursor.fetchall()

    def __get_compound_by_name(self, compound):
    
        self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE name = ?''', [compound.name])
        return self.cursor.fetchall()

    def get_compound_from_db(self, compound):

        if compound.cas:
            result_cas = self.__get_compound_by_cas(compound)
            if not result_cas:
                result_name = self.__get_compound_by_name(compound)
        if result_cas:
            result = result_cas
        else:
            result = result_name
        if len(result) == 1:
            reagent_row = result[0]
            log.info('%s is in the database', reagent_row[2])
            return reagent_row[2]
        if len(result) < 1:
            log.info('%s not in dabase', compound.cas)
            return None
        if len(result) > 1:
            raise ValueError('Duplicate values in the database')

    def get_hazards_from_reagent_id(self, reagent_id):
        result = self.cursor.execute(''' 
SELECT HAZARDS.hazard_id, HAZARDS.hazard_code, HAZARDS.hazard_description  FROM REAGENTS_HAZARDS
LEFT JOIN HAZARDS on REAGENTS_HAZARDS.hazard_id = HAZARDS.hazard_id WHERE REAGENTS_HAZARDS.reagent_id = ?''', [reagent_id])
        hazards = [Hazard(code = element[0], warning_line = element[2]) for element in result] 
        return hazards


    def get_hazard_from_db(self, hazard):
        self.cursor.execute(''' SELECT hazard_code, hazard_description, hazard_id FROM HAZARDS WHERE hazard_code = ?''', [hazard.code])
        return self.cursor.fetchall()
    
    def insert_compound_hazard(self, compound):

        reagent_list = self.get_compound_from_db(compound)

        if not reagent_list:        
            result = get_hazards(compound)
            no_cid = 'No CID found'
            if result == no_cid:
                self.cursor.execute(''' INSERT INTO REAGENTS_CAS (cas, name, found_in_pubchem) VALUES (?, ?, ?) ''', (compound.cas, compound.name,'No'))
                self.conn.commit()
            else:
                self.cursor.execute(''' INSERT INTO REAGENTS_CAS (cas, name, found_in_pubchem) VALUES (?, ?, ?) ''', (compound.cas, compound.name,'Yes',))
                self.conn.commit()
                hazards = result[0]
                log.info('%s', hazards)
                for hazard in hazards:
                    if not self.get_hazard_from_db(hazard):
                        self.cursor.execute(''' INSERT INTO HAZARDS (hazard_code, hazard_description) VALUES (?, ?) ''', (hazard.code, hazard.warning_line))
                        self.conn.commit()
        
    

               

wb = load_workbook(filename='trial_input.xlsx')
ws = wb.active
substances = []
    
read_row_index = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    read_row_index += 1
    try:
        name = row[0]
        cas = row[1]
        compound = Compound(cas, name)
        substances.append(compound)
    except Exception as e:
        log.error(e, exc_info=True)



cache = Cache(db_name)

for substance in substances:
    cache.insert_compound_hazard(substance)
    log.info('Substance %s inserted into the database', read_row_index)








