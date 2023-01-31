from flask_app import app
from flask import render_template, request, redirect

@app.route('/c')
def index():
    return render_template("c.html")