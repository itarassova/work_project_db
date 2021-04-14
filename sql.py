import json
import requests
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parser
from openpyxl import Workbook, load_workbook
import time
import logging as log
import sqlite3
from compound import Compound
from hazard import Hazard, HazardTypes
from pathlib import Path


log.basicConfig(level=log.INFO)

db_name = 'Charnwood_inventory_back-up_really_large_number.db'

class Database:
    def __init__(self,db_name):
        db_file = Path(db_name)
        new_db = db_name == ':memory:' or not db_file.is_file()
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
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
            [reagent_id] integer,
            [hazard_id] integer
            );
            ''')

        self.conn.commit()

    def __get_compound_by_cas(self, compound: Compound) -> tuple:
    
        self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE cas = ?''', [compound.cas])
        return self.cursor.fetchall()

    def get_query_by_input(self, input: str):
        query = self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE cas = ?''', [input])
        result = self.cursor.fetchall()[0]
        if not result:
            query = self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE name = ?''', [input])
            result = self.cursor.fetchall()[0]
        compound = Compound(cas=result[0], name=result[1])
        reagent_id = result[2]
        return compound, reagent_id


    def __get_compound_by_name(self, compound):
    
        self.cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE name = ?''', [compound.name])
        return self.cursor.fetchall()

    def __insert_compound(self,compound: Compound) -> int:
        self.cursor.execute(''' INSERT INTO REAGENTS_CAS (cas, name, found_in_pubchem) VALUES (?, ?, ?) ''', (compound.cas, compound.name,'Yes'))
        reagent_id = self.cursor.lastrowid
        self.conn.commit()
        return reagent_id

    def __insert_hazard(self, hazard: Hazard) -> int:
        self.cursor.execute(''' INSERT INTO HAZARDS (hazard_code, hazard_description) VALUES (?, ?) ''', (hazard.code, hazard.warning_line))
        hazard_id = self.cursor.lastrowid
        self.conn.commit()
        return hazard_id

        

    def get_reagent_id_from_db(self, compound: Compound) -> int:

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

    def __get_hazards_from_reagent_id(self, reagent_id):
        result = self.cursor.execute(''' 
SELECT HAZARDS.hazard_id, HAZARDS.hazard_code, HAZARDS.hazard_description  FROM REAGENTS_HAZARDS
LEFT JOIN HAZARDS on REAGENTS_HAZARDS.hazard_id = HAZARDS.hazard_id WHERE REAGENTS_HAZARDS.reagent_id = ?''', [reagent_id])
        hazards = [Hazard(code = element[1], warning_line = element[2]) for element in result] 
        return hazards


    def get_hazard_from_db(self, hazard: Hazard) -> int:
        self.cursor.execute(''' SELECT hazard_code, hazard_description, hazard_id FROM HAZARDS WHERE hazard_code = ?''', [hazard.code])
        result = self.cursor.fetchall()
        if len(result) == 1:
            hazard_row = result[0]
            log.info('%s is in the database', hazard_row[2])
            return hazard_row[2]
        if len(result) < 1:
            log.info('%s not in dabase', hazard.code)
            return None
        if len(result) > 1:
            raise ValueError('Duplicate values in the database')

    def __reagent_id_for_compound(self, compound):
        reagent_id = self.get_reagent_id_from_db(compound)
        if reagent_id:
            return reagent_id
        return self.__insert_compound(compound)
        # return reagent_id if reagent_id else self.__insert_compound(compound)

    def __hazard_id_for_hazard(self, hazard):
        hazard_id = self.get_hazard_from_db(hazard)
        if hazard_id:
            return hazard_id
        return self.__insert_hazard(hazard)

    def get_hazards_from_compound(self, compound):
        reagent_id = self.get_reagent_id_from_db(compound)
        if reagent_id:
            return self.__get_hazards_from_reagent_id(reagent_id)
        else:
            return None 
    
    def insert_compound_hazard(self, compound, hazards: list[Hazard]):
        reagent_id = self.__reagent_id_for_compound(compound)        
        for hazard in hazards:
            hazard_id = self.__hazard_id_for_hazard(hazard)
            self.cursor.execute(''' INSERT INTO REAGENTS_HAZARDS (reagent_id, hazard_id) VALUES (?, ?) ''', (reagent_id, hazard_id))
            self.conn.commit()
               










