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
    #Write code for verification
    if():
        flash('Login successsful', 'success')
        return redirect(url_for(''))
    else:
        flash('Invalid username or passwork', 'error')
        return redirect(url_for('auth.login_get'))

@bp.get('/logout')
def logout_get():
    #Write code to update db on username
    flash('Logout successful', 'info')
    return redirect(url_for('auth.login_get'))
