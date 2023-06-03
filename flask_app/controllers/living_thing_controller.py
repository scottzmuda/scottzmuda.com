from flask_app import app
from flask import render_template, redirect, flash,request, session
from flask_app.models import living_thing
from flask_app.utilities import time_util

@app.route('/l')
@app.route('/l/')
def living_things():
    living_things = living_thing.Living_thing.get_all()
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

    one_living_thing = living_thing.Living_thing.get_living_thing_by_time( {"time_s": living_thing_time_s} )
    one_living_thing.generate_taxonomy()
    print("TEST")
    #one_taxon = taxon.Taxon.get_taxon_by_id( {"id": one_living_thing.taxon.id} )

    if not one_living_thing:
        return redirect('/l')

    return render_template("view-living_thing.html", living_thing=one_living_thing)#, taxon=one_taxon)

@app.route('/l/create-living_thing')
def create_living_thing():
    if 'creator_id' not in session:
        return redirect('/l')
    return render_template("create-living_thing.html")

@app.route('/l/save-living_thing', methods=["POST"])
def save_living_thing():
    if 'creator_id' not in session:
        return redirect('/l')
    
    print(request.form)

    if not living_thing.Living_thing.validate_living_thing_form(request.form):
        #session['name'] = request.form['name']
        #session['name_scientific'] = request.form['name_scientific']
        #session['description'] = request.form['description']
        session['lat_deg'] = request.form['lat_deg']
        session['long_deg'] = request.form['long_deg']
        session['elev_m'] = request.form['elev_m']
        session['date_time'] = request.form['date_time']
        return redirect('/l/create-living_thing')

    check_date_time = time_util.date_time_offset_to_utc_sec(request.form['date_time'], request.form['utc_offset_minutes'])
    
    # loop for 100 tries, else flash message to user to choose new time
    count = 0
    while count < 100:
        # query to confirm we do not already have an entry for same utc time
        if not living_thing.Living_thing.get_living_thing_by_time({'time_s': check_date_time}):
            break
        check_date_time += 1
        count += 1
    
    if count >= 100:
        flash('database is full for that timestamp, please select a different timestamp for your post', "create_living_thing")
        #session['name'] = request.form['name']
        #session['name_scientific'] = request.form['name_scientific']
        #session['description'] = request.form['description']
        session['lat_deg'] = request.form['lat_deg']
        session['long_deg'] = request.form['long_deg']
        session['elev_m'] = request.form['elev_m']
        session['date_time'] = request.form['date_time']
        return redirect('/l/create-living_thing')

    data = {
        "creator_id": session['creator_id'],
        #"name": request.form['name'],
        #"name_scientific": request.form['name_scientific'],
        #"description": request.form['description'],
        "lat_deg": request.form['lat_deg'],
        "long_deg": request.form['long_deg'],
        "elev_m": request.form['elev_m'],
        "time_s": check_date_time
    }

    living_thing_id = living_thing.Living_thing.save( data )
    one_living_thing = living_thing.Living_thing.get_living_thing_by_id( {"id": living_thing_id} )

    hold_creator_id = session['creator_id']
    session.clear()
    session['creator_id'] = hold_creator_id

    return redirect('/l/'+one_living_thing.url_string)