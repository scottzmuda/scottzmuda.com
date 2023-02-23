from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import living_thing

@app.route('/l')
@app.route('/l/')
def living_things():
    living_things = living_thing.living_thing.get_all()
    return render_template("index-living_things.html", living_things=living_things)

@app.route('/l/<living_thing_url>')
def view_living_thing( living_thing_url ):
    
    living_thing_time_s = 0

    # check character by character until we find a "-"
    # then slice the part of the string before the "-"
    for i in range(len(living_thing_url)):
        next_char = living_thing_url[i]
        if next_char == "-":
            living_thing_time_s = living_thing_url[:i]
            break
    

    # safety checks for handling our url string
    # just in case someone manually types in a url
    # if living_thing_time_s is still 0 OR if we have a non decimal (0-9) expression
    # then we safely redirect to the living_thingdex page
    if not living_thing_time_s or not living_thing_time_s.isdecimal():
        return redirect('/l')
    
    # else cast numeric string "12345" -> 12345
    living_thing_time_s = int(living_thing_time_s)

    one_living_thing = living_thing.living_thing.get_living_thing_by_time( {"time_s": living_thing_time_s} )

    if not one_living_thing:
        return redirect('/l')

    return render_template("view-living_thing.html", living_thing=one_living_thing )

@app.route('/l/create-living_thing')
def create_living_thing():
    if 'creator_id' not in session:
        return redirect('/l')
    return render_template("create-living_thing.html")

@app.route('/l/save-living_thing', methods=["POST"])
def save_living_thing():
    if 'creator_id' not in session:
        return redirect('/l')
    data = {
        "name": request.form["name"],
        "name_scientific": request.form["name_scientific"],
        "description": request.form["description"],
        "lat_deg": request.form["lat_deg"],
        "long_deg": request.form["long_deg"],
        "elev_m": request.form["elev_m"],
        "time_s": request.form["time_s"]
    }
    living_thing.living_thing.save( data )
    return redirect('/l/create-living_thing')