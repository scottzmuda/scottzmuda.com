from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import writing

@app.route('/w')
def writings():
    return render_template("w.html")

@app.route('/w/add-writing')
def draft_new_writing():
    return render_template("add-writing.html")

@app.route('/w/save-writing', methods=["POST"])
def save_new_writing():
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "content": request.form["content"],
    }

    writing.Writing.save( data )
    return redirect('/w/add-writing')