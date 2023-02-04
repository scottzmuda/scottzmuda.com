from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import writing

@app.route('/w')
@app.route('/w/')
def writings():
    return render_template("writingdex.html")

@app.route('/w/create-writing')
def create_writing():
    return render_template("create-writing.html")

@app.route('/w/save-writing', methods=["POST"])
def save_writing():
    data = {
        "name": request.form["name"],
        "image": request.form["image"],
        "writing": request.form["writing"],
        "description": request.form["description"],
    }

    writing.writing.save( data )
    return redirect('/w/create-writing')