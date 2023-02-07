from flask_app import app
from flask import render_template, redirect
from flask_app.models import creature

@app.route('/c/<creature_url>')
def view_creature( creature_url ):
    
    creature_time_s = 0

    # check character by character until we find a "_"
    # then slice the part of the string before the "_"
    for i in range(len(creature_url)):
        next_char = creature_url[i]
        if next_char == "-":
            creature_time_s = creature_url[:i]
            break
    

    # safety checks for handling our url string
    # just in case someone manually types in a url
    # if creature_time_s is still 0 OR if we have a non decimal (0-9) expression
    # then we safely redirect to the creaturedex page
    if not creature_time_s or not creature_time_s.isdecimal():
        return redirect('/c')
    
    # else cast numeric string "12345" -> 12345
    creature_time_s = int(creature_time_s)

    one_creature = creature.Creature.get_creature_by_time( {"time_s": creature_time_s} )
    return render_template("view-creature.html", creature=one_creature )