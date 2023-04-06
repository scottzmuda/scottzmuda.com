from flask_app import app
from flask import render_template, redirect, request, session

@app.route('/c')
@app.route('/c/')
def conversations():
    return render_template("index-conversations.html")