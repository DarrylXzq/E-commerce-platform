import hashlib

import mysql.connector
from db_config import db_connection
from flask import jsonify, request, session, redirect, url_for, render_template, Blueprint

login = Blueprint('login', __name__)


# Login page
@login.route('/login_page')
def login_page():
    return render_template("login.html")


# Check login
@login.route('/check_login', methods=['POST'])
def check_login():
    username = request.form.get('username')
    password = request.form.get('password')
    captcha = request.form.get('captcha')
    real_captcha = request.cookies.get('captcha')
    user_type = request.form.get('user_type')

    errors = {}
    if not captcha:
        errors['captcha'] = 'Captcha is required!'
    elif not real_captcha:
        errors['captcha'] = 'Captcha timed out. Please refresh and try again!'
    elif captcha.upper() != real_captcha:
        errors['captcha'] = 'Incorrect captcha. Please try again!'

    if not username:
        errors['username'] = 'Username is required!'

    if not password:
        errors['password'] = 'Password is required!'

    if not user_type:
        errors['user_type'] = 'Please select a user type!'

    if not errors:
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to the database
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        # Query the database based on user_type
        if user_type == "customer":
            query = "SELECT * FROM customers WHERE name = %s AND password = %s"
        elif user_type == "vendor":
            query = "SELECT * FROM vendors WHERE vendor_name = %s AND password = %s"

        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        if not user:
            errors['login'] = 'Invalid username or password. Please try again!'
            return jsonify(success=False, errors=errors, show_alert=True)

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        session['user_type'] = user_type
        session['user_id'] = user[0]
        return jsonify(success=True)


# After login
@login.route('/after_login')
def after_login():
    return redirect(url_for('index'))


# Logout
@login.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
