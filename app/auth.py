from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# from db import select_query, insert_query
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

bp = Blueprint('auth', __name__, url_prefix='/auth')
DB_FILE = "Lebron.db"

@bp.get('/signup')
def signup_get():
    return render_template('signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    confirm = request.form.get('confirm')
    if (password != confirm):
        flash('Passwords must match', 'error')
        return redirect(url_for('auth.signup_get'))
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("select * from users where username = ?", (username,))
    user_exists = c.fetchone()
    if user_exists:
        flash('Username already taken', 'error')
        return redirect(url_for('auth.signup_get'))
    hashword = generate_password_hash(password)
    c.execute("insert into users (username, password) values (?, ?)", (username, hashword))
    db.commit()
    db.close()
    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():
    return render_template('login.html')

@bp.post('/login')
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("select password from users where username = ?", (username,))
    user_data = c.fetchone()
    if(user_data):
        hashword = user_data[0]
        if(check_password_hash(hashword, password)):
            # this bottom flash would display the message on the next load of login but i assume we want it on homepage instead
            # flash('Login successsful', 'success')
            session["username"] = username
            return redirect(url_for('disp_homepage'))
        else:
            flash('Invalid password', 'error')
            return redirect(url_for('auth.login_get'))
    else:
        flash("Username incorrect or not found", 'error')
        return redirect(url_for('auth.login_get'))

@bp.get('/logout')
def logout_get():
    #Write code to update db on username
    session.pop('username', None)
    flash('Logout successful', 'success')
    return redirect(url_for('auth.login_get'))
