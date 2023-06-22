import hashlib

import mysql.connector
from db_config import db_connection
from flask import Blueprint, render_template, session, redirect, url_for, request

vendor_info = Blueprint('vendor_info', __name__)


# encrypt the password
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()


# vendor mail page
@vendor_info.route('/mail_page')
def mail_page():
    vendor_id = session.get('user_id')
    if not vendor_id:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = "SELECT * FROM addresses_vendor WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))

    address = cursor.fetchone()
    if address:
        address = {
            'address_id': address[0],
            'vendor_id': address[1],
            'country_name': address[2],
            'province_name': address[3],
            'city_name': address[4],
            'address': address[5]
        }

    cursor.close()
    connection.close()
    message = session.pop('message', None)

    return render_template("vendor_mail.html", message=message, address=address)


# update the vendor address
@vendor_info.route('/update_vendor_address', methods=['POST'])
def update_vendor_address():
    if request.method == 'POST':
        address_id = request.form['address_id']
        country_name = request.form['country_name']
        province_name = request.form['province_name']
        city_name = request.form['city_name']
        address = request.form['address']

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        if address_id:
            query = """
            UPDATE addresses_vendor
            SET country_name = %s, province_name = %s, city_name = %s, address = %s
            WHERE address_id = %s
            """
            cursor.execute(query, (country_name, province_name, city_name, address, address_id))
        else:
            vendor_id = session.get('user_id')
            query = """
            INSERT INTO addresses_vendor (vendor_id, country_name, province_name, city_name, address)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (vendor_id, country_name, province_name, city_name, address))

        connection.commit()
        cursor.close()
        connection.close()
        session['message'] = 'Update successful'

        return redirect(url_for('vendor_info.mail_page'))

    session['message'] = 'Update failed'
    return redirect(url_for('vendor_info.mail_page'))


# vendor personal info page
@vendor_info.route('/personal_info')
def personal_info():
    vendor_id = session.get('user_id')
    if not vendor_id:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = "SELECT * FROM vendors WHERE vendor_id = %s"
    cursor.execute(query, (vendor_id,))

    vendor = cursor.fetchone()
    if vendor:
        vendor = {
            'vendor_id': vendor[0],
            'vendor_name': vendor[1],
            'vendor_email': vendor[3],
            'vendor_phone': vendor[4],
        }

    cursor.close()
    connection.close()

    message = session.pop('message', None)
    message_name = session.pop('message-name', None)
    message_email = session.pop('message-email', None)
    message_phone = session.pop('message-phone', None)
    return render_template("vendor_personal_info.html", vendor=vendor, message=message, message_name=message_name,
                           message_email=message_email, message_phone=message_phone)


# update the vendor personal info
@vendor_info.route('/update_personal_info', methods=['POST'])
def update_personal_info():
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        vendor_email = request.form['vendor_email']
        vendor_phone = request.form['vendor_phone']
        vendor_password = request.form['vendor_password']

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        # check the name
        query = """
               SELECT vendor_name FROM vendors
               WHERE vendor_name = %s  AND vendor_id != %s
               """
        cursor.execute(query, (vendor_name, vendor_id))
        duplicate_vendor = cursor.fetchone()
        if duplicate_vendor:
            session['message-name'] = 'the name has been registered'
            return redirect(url_for('vendor_info.personal_info'))

        # check the email
        query = """
        SELECT email FROM vendors
        WHERE email = %s  AND vendor_id != %s
        """
        cursor.execute(query, (vendor_email, vendor_id))
        duplicate_vendor = cursor.fetchone()
        if duplicate_vendor:
            session['message-email'] = 'the email has been registered'
            return redirect(url_for('vendor_info.personal_info'))

        # check the phone
        query = """
                SELECT phone FROM vendors
                WHERE phone = %s  AND vendor_id != %s
                """
        cursor.execute(query, (vendor_phone, vendor_id))
        duplicate_vendor = cursor.fetchone()
        if duplicate_vendor:
            session['message-phone'] = 'the phone has been registered'
            return redirect(url_for('vendor_info.personal_info'))

        # update the vendor info
        if vendor_password:
            # if the password is not empty, hash the password
            hashed_password = hash_password(vendor_password)
            query = """
                UPDATE vendors
                SET vendor_name = %s, email = %s, phone = %s, password = %s
                WHERE vendor_id = %s
                """
            cursor.execute(query, (vendor_name, vendor_email, vendor_phone, hashed_password, vendor_id))
        else:
            query = """
                UPDATE vendors
                SET vendor_name = %s, email = %s, phone = %s
                WHERE vendor_id = %s
                """
            cursor.execute(query, (vendor_name, vendor_email, vendor_phone, vendor_id))

        connection.commit()
        cursor.close()
        connection.close()

        session['message'] = 'Update successful'
        return redirect(url_for('vendor_info.personal_info'))

    return redirect(url_for('vendor_info.personal_info'))
