import hashlib
import os
import re

import mysql.connector
from db_config import db_connection
from flask import jsonify, request, session, redirect, url_for, render_template, Blueprint, current_app
from werkzeug.utils import secure_filename

nav_user = Blueprint('nav_user', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# check the file format
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# encrypt the password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


# ================personal information edit page===================
@nav_user.route('/update_info')
def update_info():
    return render_template('user_edit.html')


@nav_user.route('/get_customer_info', methods=['GET'])
def get_customer_info():
    if 'user_id' in session:
        customer_id = session['user_id']

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()
        query = "SELECT * FROM customers WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            customer_info = {
                'customer_id': result[0],
                'username': result[1],
                'email': result[3],
                'phone': result[4],
                'birthday': result[5],
                'gender': result[6],
                'avatar_path': result[8],
            }
            return jsonify(customer_info)
    return jsonify({})


@nav_user.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'file' not in request.files:
        return jsonify(success=False, error='No file part')

    file = request.files['file']
    if file.filename == '':
        return jsonify(success=False, error='No selected file')

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Update user avatar path in the database
        user_id = session['user_id']
        conn = mysql.connector.connect(**db_connection)
        cursor = conn.cursor()

        query = "UPDATE customers SET avatar = %s WHERE customer_id = %s"
        cursor.execute(query, (file_path, user_id))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, filename=filename)

    return jsonify(success=False, error='Invalid file format')


@nav_user.route('/update', methods=['POST'])
def update():
    if 'user_id' in session:
        customer_id = session['user_id']

        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        password = request.form.get('password')

        errors = {}

        if not username:
            errors['username'] = 'Username is required!'

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

        if password:
            password_pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
            if not password_pattern.match(password):
                errors[
                    'password'] = 'must have: 1 uppercase, 1 lowercase, 1 number, 1 special character, and be 8+ characters long.'

        if errors:
            return jsonify(errors=errors)

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        # Check if the phone is unique
        query = "SELECT * FROM customers WHERE phone = %s AND customer_id != %s"
        cursor.execute(query, (phone, customer_id))
        user = cursor.fetchone()
        if user:
            errors['phone'] = 'Phone number already exists!'

        # Check if the username is unique
        query = "SELECT * FROM customers WHERE name = %s AND customer_id != %s"
        cursor.execute(query, (username, customer_id))
        user = cursor.fetchone()
        if user:
            errors['username'] = 'Username already exists!'

        query = "SELECT * FROM customers WHERE email = %s AND customer_id != %s"
        cursor.execute(query, (email, customer_id))
        user = cursor.fetchone()
        if user:
            errors['email'] = 'Email already exist'

        if errors:
            cursor.close()
            connection.close()
            return jsonify(errors=errors)

        else:
            hashed_password = hash_password(password)
            if birthday and password:
                query = "UPDATE customers SET name = %s, password=%s, email = %s, phone = %s, birthday = %s, gender = %s WHERE customer_id = %s"
                cursor.execute(query, (username, hashed_password, email, phone, birthday, gender, customer_id))
            elif password and not birthday:
                query = "UPDATE customers SET name = %s, password = %s, email = %s, phone = %s, birthday = NULL, gender = %s WHERE customer_id = %s"
                cursor.execute(query, (username, hashed_password, email, phone, gender, customer_id))
            elif birthday and not password:
                query = "UPDATE customers SET name = %s, email = %s, phone = %s, birthday = %s, gender = %s WHERE customer_id = %s"
                cursor.execute(query, (username, email, phone, birthday, gender, customer_id))
            else:
                query = "UPDATE customers SET name = %s, email = %s, phone = %s, birthday = NULL, gender = %s WHERE customer_id = %s"
                cursor.execute(query, (username, email, phone, gender, customer_id))

        connection.commit()
        cursor.close()
        connection.close()
        return jsonify(success=True)
    else:
        return redirect(url_for('login.login_page'))


# ==================update mailing information====================

@nav_user.route('/mail_info')
def mail_info():
    return render_template('user_mail.html')


@nav_user.route('/get_mail_info', methods=['GET', 'POST'])
def get_mail_info():
    if 'user_id' in session:
        if request.method == 'POST':
            index = int(request.form.get('index', 0))

            customer_id = session['user_id']

            connection = mysql.connector.connect(**db_connection)
            cursor = connection.cursor()
            query = "SELECT * FROM addresses_customer WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()

            if 0 <= index < len(result):
                return jsonify(result[index])
            else:
                return jsonify({'error': 'Invalid index'}), 400

        return render_template('user_mail.html')

    return render_template('user_mail.html')


@nav_user.route('/update_mail_info', methods=['POST'])
def update_mail_info():
    if 'user_id' in session:
        customer_id = session['user_id']

        username = request.form.get('username')
        phone = request.form.get('phone')
        country = request.form.get('country')
        province = request.form.get('province')
        city = request.form.get('city')
        address = request.form.get('address')
        address_id = request.form.get('address_id')

        errors = {}

        if not username:
            errors['username'] = 'Username is required!'

        if not phone:
            errors['phone'] = 'Phone number is required!'
        else:
            phone_pattern = re.compile('^\+?\d{1,4}[-\s]?\(?\d{1,3}?\)?[-\s]?\d{1,4}[-\s]?\d{1,4}[-\s]?\d{1,9}$')
            if not phone_pattern.match(phone):
                errors['phone'] = 'Invalid phone number format!'

        if not country:
            errors['country'] = 'Country is required!'

        if not province:
            errors['province'] = 'Province is required!'

        if not city:
            errors['city'] = 'City is required!'
        if not address:
            errors['address'] = 'Address is required!'

        if errors:
            return jsonify(errors=errors)

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        if address_id:
            query = "UPDATE addresses_customer SET receiver_name = %s, receiver_phone = %s, " \
                    "country_name = %s, province_name = %s, city_name = %s, address = %s " \
                    "WHERE customer_id = %s AND address_id = %s"
            cursor.execute(query, (username, phone, country, province, city, address, customer_id, address_id))
        else:
            query = "INSERT INTO addresses_customer (receiver_name, receiver_phone, " \
                    "country_name, province_name, city_name, address, customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (username, phone, country, province, city, address, customer_id))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify(success=True)
    else:
        return redirect(url_for('login.login_page'))


@nav_user.route('/get_address_count', methods=['GET'])
def get_address_count():
    if 'user_id' in session:
        customer_id = session['user_id']

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM addresses_customer WHERE customer_id = %s"
        cursor.execute(query, (customer_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        connection.close()

        return str(count)

    return "0"


@nav_user.route('/delete_address', methods=['POST'])
def delete_address():
    if 'user_id' in session:
        address_id = request.form.get('address_id')
        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()
        query = "DELETE FROM addresses_customer WHERE address_id = %s"
        cursor.execute(query, (address_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify(success=True)
    else:
        return redirect(url_for('login.login_page'))


# ==================check information page====================

@nav_user.route('/info')
def info():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login.login_page'))

    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    query = "SELECT customer_id, name, email, phone, gender, registration_c, avatar FROM customers WHERE customer_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        customer_id, username, email, phone, gender, registration_c, avatar_path = result
        avatar_path = '../' + avatar_path
        return render_template("customer_info.html", username=username, email=email, phone=phone,
                               avatar_path=avatar_path, customer_id=customer_id, gender=gender,
                               registration=registration_c)
    else:
        return "User not found", 404
