from flask_app import app
from flask import render_template, request, redirect

@app.route('/index')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/browserconfig.xml')
@app.route('/favicon.ico')
@app.route('/humans.txt')
@app.route('/robots.txt')
@app.route('/site.webmanifest')
def static_from_root():
    return app.send_static_file(request.path[1:])

@app.route('/.well-known/nostr.json')
def nostr_static_from_root():
    return app.send_static_file('nostr.json')