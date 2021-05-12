from flask import Flask, render_template, g, request
import sqlite3
from compound import Compound
from hazard import Hazard
from datetime import date
import json


def get_db():
    db = getattr(g, '_number', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_compound_by_input(input: str, cursor) -> (Compound, int):
    query = cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE cas = ?''', [input])
    query_result = cursor.fetchall()
    if not query_result:
        query = cursor.execute(''' SELECT cas, name, reagent_id FROM REAGENTS_CAS WHERE name = ?''', [input])
        query_result = cursor.fetchall()
        if not query_result:
            return None, None
    result = query_result[0]   
    compound = Compound(cas=result[0], name=result[1])
    reagent_id = result[2] 
    return compound, reagent_id


def get_cas_list_from_input(input: str, cursor):
    query = cursor.execute(''' SELECT cas FROM REAGENTS_CAS WHERE cas LIKE ? ORDER BY cas ASC''', [input+'%'])
    query_result = cursor.fetchall()
    if not query_result:
        query = cursor.execute(''' SELECT cas FROM REAGENTS_CAS WHERE name = ? ORDER BY cas ASC''', [input+'%'])
        query_result = cursor.fetchall()
        if not query_result:
            return None, None
    cas_list = []
    for query in query_result:
        cas_list.append(query[0])

    return cas_list



def get_hazards_by_reagent_id(reagent_id: int, cursor) -> [Hazard]:
    query_hazards = cursor.execute(''' 
SELECT HAZARDS.hazard_id, HAZARDS.hazard_code, HAZARDS.hazard_description  FROM REAGENTS_HAZARDS
LEFT JOIN HAZARDS on REAGENTS_HAZARDS.hazard_id = HAZARDS.hazard_id WHERE REAGENTS_HAZARDS.reagent_id = ?''', [reagent_id])
    hazards = [Hazard(code = element[1], warning_line = element[2]) for element in query_hazards] 
    return hazards
    


DATABASE = 'Charnwood_inventory_back-up_really_large_number.db'

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_number', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def form():
    reagents = ['98-98-6', '110-86-1']
    return render_template('form.html', compounds = reagents)

@app.route('/form', methods=['GET'])
def fill_form():
    # http://localhost:5000/form?compound+1=98-98-6&compound+2=110-86-1
    # request.args = {"compound+1": "98-98-6", "compound+2":"110-86-1"}
    # for key, value in request.args:
    # for value in request.args.values():
    value = request.args.get('compound',)
    input = value.split(", ")
    cursor = get_db().cursor()
    reagents = {}
    for entry in input:
        compound, reagent_id = get_compound_by_input(entry, cursor)
        if not compound:
            return render_template('notfound.html', identifier = input, db = DATABASE)
        hazards = get_hazards_by_reagent_id(reagent_id, cursor)
        reagents[compound] = hazards
    mytime = date.today()
   
    return render_template('coshh.html', reagents = reagents, key = compound,date = mytime) 

@app.route('/lookup', methods=['GET']) 

def get_cas_list():
    # http://localhost:5000/form?compound+1=98-98-6&compound+2=110-86-1
    # request.args = {"compound+1": "98-98-6", "compound+2":"110-86-1"}
    # for key, value in request.args:
    # for value in request.args.values():
    input = request.args.getlist('compound',)
    cursor = get_db().cursor()
    query_list = []
    for entry in input:
        query_list.extend(get_cas_list_from_input(entry, cursor))
    if not query_list:
        return render_template('notfound.html', identifier = input, db = DATABASE)
    selector = json.dumps(query_list)

    return selector

if __name__ == '__main__':
    app.run(debug = True)