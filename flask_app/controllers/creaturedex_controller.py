from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import creature

@app.route('/c')
@app.route('/c/')
def creatures():
    creatures = creature.Creature.get_all()
    return render_template("creaturedex.html", creatures=creatures)