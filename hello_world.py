from flask import Flask, render_template
from compound import Compound
from sql import Database

db_name = 'Charnwood_inventory_back-up_really_large_number.db'
cache = Database(db_name)

app = Flask(__name__)

@app.route('/compound/<input>')
def show_compound(input):
    compound, reagent_id = cache.get_query_by_input(input)
    return render_template('hello.html', cas = compound.cas, name = compound.name, reagent_id = reagent_id)  
if __name__ == '__main__':
    app.run(debug = True)