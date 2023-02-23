from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models import creator

@app.route('/c/registration')
def registration_form():
    # protect registration form, so account cannot be created if there is
    # already someone logged in
    if 'creator_id' in session:
        return redirect('/')
    return render_template("registration.html")

@app.route('/c/register-creator', methods=["POST"])
def register_new_creator():

    if not creator.Creator.validate_registration_form(request.form):
        session['name'] = request.form['name']
        session['name_id'] = request.form['name_id']
        session['email'] = request.form['email']
        return redirect('/c/registration')
    
    data = {
        "name": request.form['name'],
        "name_id": request.form['name_id'],
        "email": request.form['email'],
        "password_hash": creator.Creator.hash_password(request.form),
    }

    session.clear()
    session['creator_id'] = creator.Creator.save(data)
    return redirect('/')

@app.route('/c/login')
def login_form():
    if 'creator_id' in session:
        return redirect('/')
    return render_template("login.html")

@app.route('/c/log-creator-in', methods=["POST"])
def log_user_in():
    if not creator.Creator.validate_login_form(request.form):
        session['email_login'] = request.form['email']
        return redirect('/c/login')
    
    creator_id = creator.Creator.verify_login_credentials(request.form)
    if not creator_id:
        session['email_login'] = request.form['email']
        return redirect('/c/login')

    session['creator_id'] = creator_id
    return redirect('/')

@app.route('/c/log-creator-out')
def log_creator_out():
    session.clear()
    return redirect('/')
