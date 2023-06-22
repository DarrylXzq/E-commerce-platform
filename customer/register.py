import hashlib
import re

import mysql.connector
from db_config import db_connection
from flask import jsonify, request, session, render_template, Blueprint, redirect, url_for

register = Blueprint('register', __name__)


# encrypt the password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


# register page
@register.route('/register_page')
def register_page():
    return render_template("register.html")


# check the register information
@register.route('/check_register', methods=['POST'])
def check_register():
    username = request.form.get('username')
    password = request.form.get('password')
    captcha = request.form.get('captcha')
    real_captcha = request.cookies.get('captcha')
    user_type = request.form.get('user_type')
    phone = request.form.get('phone')
    email = request.form.get('email')

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
    else:
        password_pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        if not password_pattern.match(password):
            errors[
                'password'] = 'must have: 1 uppercase, 1 lowercase, 1 number, 1 special character, and be 8+ characters long.'
    if not user_type:
        errors['user_type'] = 'Please select a user type!'

    if not phone:
        errors['phone'] = 'Phone number is required!'
    else:
        phone_pattern = re.compile('^\+?\d{1,4}[-\s]?\(?\d{1,3}?\)?[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{1,9}$')
        if not phone_pattern.match(phone):
            errors['phone'] = 'Invalid phone number format!'

    if not email:
        errors['email'] = 'Email is required!'
    else:
        email_pattern = re.compile('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            errors['email'] = 'Invalid email format. Please try again!'

    if not errors:
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        # Check if the email is unique
        if user_type == 'customer':
            query = "SELECT * FROM customers WHERE email = %s"
        else:
            query = "SELECT * FROM vendors WHERE email = %s"

        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user:
            errors['email'] = 'Email already exists!'

        # Check if the phone is unique
        if user_type == 'customer':
            query = "SELECT * FROM customers WHERE phone = %s"
        else:
            query = "SELECT * FROM vendors WHERE phone = %s"

        cursor.execute(query, (phone,))
        user = cursor.fetchone()

        if user:
            errors['phone'] = 'Phone number already exists!'

        # Check if the username is unique
        if user_type == 'customer':
            query = "SELECT * FROM customers WHERE name = %s"
        else:
            query = "SELECT * FROM vendors WHERE vendor_name = %s"

        cursor.execute(query, (username,))
        user = cursor.fetchone()

        if user:
            errors['username'] = 'Username already exists!'

        # If no errors, insert the new user
        if not errors:
            hashed_password = hash_password(password)
            if user_type == 'customer':
                default_avatar_path = '../static/uploads/default_avatar.png'
                query = "INSERT INTO customers (name, password, email, phone, avatar) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(query, (username, hashed_password, email, phone, default_avatar_path))
            else:
                # ==============================the vendor avatar================================
                default_avatar_path = '../static/uploads/default_avatar.png'
                query = "INSERT INTO vendors (vendor_name, password, email, phone) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (username, hashed_password, email, phone))
        conn.commit()
        cursor.close()
        conn.close()

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        session['user_type'] = user_type
        session['user_id'] = cursor.lastrowid
        return jsonify(success=True)


# after register
@register.route('/after_register')
def after_register():
    if session.get('user_type') == 'customer':
        return redirect(url_for('index'))
    elif session.get('user_type') == 'vendor':
        return redirect(url_for('vendor_upload.upload_page'))
