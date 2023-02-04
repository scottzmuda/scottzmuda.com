from flask_app import app
from flask import render_template
from flask_app.models import creature

@app.route('/c/<int:creature_id>')
def view_creature( creature_id ):
    one_creature = creature.Creature.get_creature_by_id( {"id": creature_id} )
    return render_template("view-creature.html", creature=one_creature )