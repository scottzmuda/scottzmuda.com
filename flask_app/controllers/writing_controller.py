from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import writing

@app.route('/w')
@app.route('/w/')
def writings():
    writings = writing.Writing.get_all()
    return render_template("index-writings.html", writings=writings)

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

    one_writing = writing.Writing.get_writing_by_time( {"time_s": writing_time_s} )

    if not one_writing:
        return redirect('/w')

    return render_template("view-writing.html", writing=one_writing )

@app.route('/w/create-writing')
def create_writing():
    if 'creator_id' not in session:
        return redirect('/w')
    return render_template("create-writing.html")

@app.route('/w/save-writing', methods=["POST"])
def save_writing():
    if 'creator_id' not in session:
        return redirect('/w')
    data = {
        "name": request.form["name"],
        "writing": request.form["writing"],
        "description": request.form["description"],
        "time_s": request.form["time_s"],
    }

    writing.Writing.save( data )
    return redirect('/w/create-writing')