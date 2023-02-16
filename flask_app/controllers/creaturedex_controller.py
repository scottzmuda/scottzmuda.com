from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import creature

@app.route('/c')
@app.route('/c/')
def creatures():
    creatures = creature.Creature.get_all()
    return render_template("creaturedex.html", creatures=creatures)

@app.route('/c/create-creature')
def create_creature():
    return render_template("create-creature.html")

@app.route('/c/save-creature', methods=["POST"])
def save_creature():
    data = {
        "name": request.form["name"],
        "name_scientific": request.form["name_scientific"],
        "description": request.form["description"],
        "lat_deg": request.form["lat_deg"],
        "long_deg": request.form["long_deg"],
        "elev_m": request.form["elev_m"],
        "time_s": request.form["time_s"]
    }
    creature.Creature.save( data )
    return redirect('/c/create-creature')