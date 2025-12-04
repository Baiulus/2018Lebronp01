from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import select_query, insert_query
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.get('/signup')
def signup_get():
    return render_template('auth/signup.html')

@bp.post('/signup')
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    #Write code for adding to db
    return redirect(url_for('auth.login_get'))

@bp.get('/login')
def login_get():
    return render_template('auth/login.html')

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
