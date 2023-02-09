from flask_app import app
from flask import render_template, redirect
from flask_app.models import writing

@app.route('/w/<writing_url>')
def view_writing( writing_url ):
    
    writing_time_s = 0

    # check character by character until we find a "-"
    # then slice the part of the string before the "-"
    for i in range(len(writing_url)):
        next_char = writing_url[i]
        if next_char == "-":
            writing_time_s = writing_url[:i]
            break
    

    # safety checks for handling our url string
    # just in case someone manually types in a url
    # if writing_time_s is still 0 OR if we have a non decimal (0-9) expression
    # then we safely redirect to the writingdex page
    if not writing_time_s or not writing_time_s.isdecimal():
        return redirect('/w')
    
    # else cast numeric string "12345" -> 12345
    writing_time_s = int(writing_time_s)

    one_writing = writing.writing.get_writing_by_time( {"time_s": writing_time_s} )

    if not one_writing:
        return redirect('/w')

    return render_template("view-writing.html", writing=one_writing )