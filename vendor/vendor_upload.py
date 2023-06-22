import os
import time

import mysql.connector
from db_config import db_connection
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, current_app, session
from werkzeug.utils import secure_filename

vendor_upload = Blueprint('vendor_upload', __name__)


# find all the categories
def get_categories(parent_id=None):
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    if parent_id is None:
        cursor.execute("SELECT category_id, category_name FROM categories WHERE parent_id IS NULL")
    else:
        cursor.execute("SELECT category_id, category_name FROM categories WHERE parent_id = %s", (parent_id,))

    result = [{"category_id": row[0], "category_name": row[1]} for row in cursor.fetchall()]
    cursor.close()
    connection.close()

    return result


@vendor_upload.route('/upload_page')
def upload_page():
    return render_template("vendor_upload.html")


@vendor_upload.route('/get_parent_categories')
def get_parent_categories():
    parent_categories = get_categories()
    return jsonify(parent_categories)


@vendor_upload.route('/get_sub_categories/<int:parent_id>')
def get_sub_categories(parent_id):
    sub_categories = get_categories(parent_id)
    return jsonify(sub_categories)


# upload the file and upload the data to database
@vendor_upload.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if session.get('user_type') == 'vendor':
            vendor_id = session.get('user_id')
        else:
            return redirect(url_for('login.login_page'))

        # check if the post request has the file part
        file = request.files.get('image', None)
        new_filename = None
        if file and file.filename != '':
            # create a new filename
            timestamp = str(int(time.time()))
            _, file_ext = os.path.splitext(file.filename)
            new_filename = timestamp + '-' + str(vendor_id) + file_ext
            new_filename = secure_filename(new_filename)

            save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'products')
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)
            save_path = os.path.join(save_directory, new_filename)

            # save the file
            file.save(save_path)

            new_filename = current_app.config['UPLOAD_PRODUCT'] + '/' + new_filename

        # get the form data
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        stock = request.form['stock']
        category_id = request.form['sub_category']
        promotion = request.form.get('promotion', None)
        duration_start = request.form.get('start_date', None)
        duration_end = request.form.get('end_date', None)
        product_status = request.form['status']

        try:
            # connect to database
            connection = mysql.connector.connect(**db_connection)
            cursor = connection.cursor()
            query = """
            INSERT INTO products
            (vendor_id, category_id, name, description, price, stock, picture, promotion, duration_start, duration_end, product_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                vendor_id, category_id, name, description, price, stock, new_filename, promotion, duration_start,
                duration_end, product_status))
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({"success": True})

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return redirect(request.url)
