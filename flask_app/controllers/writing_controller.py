from flask_app import app
from flask import render_template, request, redirect
from flask_app.models import writing

@app.route('/writings/writing-form')
def draft_new_writing():
    return render_template("new-writing-form.html")

@app.route('/writings/save-new-writing', methods=["POST"])
def save_new_writing():
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "content": request.form["content"],
    }

    writing.Writing.save( data )
    return redirect('/writings/writing-form')