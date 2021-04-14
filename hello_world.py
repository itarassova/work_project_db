from flask import Flask, render_template, g
import sqlite3
from compound import Compound
from hazard import Hazard
from sql import Database



def get_db():
    db = getattr(g, '_number', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

DATABASE = 'Charnwood_inventory_back-up_really_large_number.db'
cache = Database(DATABASE)

app = Flask(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_number', None)
    if db is not None:
        db.close()



@app.route('/compound/<input>')
def show_compound(input):
    cur = get_db().cursor()
    compound, reagent_id = cache.get_query_by_input(input)
    hazards = cache.get_hazards_from_compound(compound)
    list_of_hazards = [{hazard.code : hazard.warning_line} for hazard in hazards]
    codes = [hazard.code for hazard in hazards]
    warnings = [hazard.warning_line for hazard in hazards]

    return render_template('hello.html', cas = compound.cas, name = compound.name, reagent_id = reagent_id, items = list_of_hazards, code =  )  
if __name__ == '__main__':
    app.run(debug = True)