from flask_app import app
from flask import render_template, request, redirect

@app.route('/c')
@app.route('/c/')
def creatures():
    return render_template("creaturedex.html")