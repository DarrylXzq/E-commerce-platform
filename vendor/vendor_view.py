import os
import time
from datetime import datetime

import mysql.connector
from db_config import db_connection
from flask import Blueprint, jsonify, render_template, session, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

vendor_view = Blueprint('vendor_view', __name__)


def format_datetime(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S')


@vendor_view.route('/view_page')
def view_page():
    return render_template("products_view.html")


@vendor_view.route('/vendor_edit')
def vendor_edit():
    return render_template("vendor_edit.html")


@vendor_view.route('/vendor_products', methods=['GET'])
def vendor_products():
    vendor_id = session.get('user_id')  # get vendor ID from session
    if not vendor_id:
        return jsonify({"error": "No vendor ID in session."}), 400

    # connect to database
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor(dictionary=True)

    query = '''
        SELECT * FROM products
        WHERE vendor_id = %s
        ORDER BY release_date DESC
    '''
    cursor.execute(query, (vendor_id,))

    products = cursor.fetchall()
    for product in products:
        product['release_date'] = format_datetime(product['release_date'])
        product['duration_start'] = format_datetime(product['duration_start'])
        product['duration_end'] = format_datetime(product['duration_end'])
    cursor.close()
    connection.close()

    # return products as JSON
    return jsonify(products)


@vendor_view.route('/edit_product/<int:product_id>', methods=['GET'])
def edit_product(product_id):
    if not product_id:
        return jsonify({"error": "No product ID provided."}), 400

    # access database
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor(dictionary=True)

    query = '''
        SELECT * FROM products
        WHERE product_id = %s
    '''
    cursor.execute(query, (product_id,))
    product = cursor.fetchone()

    query = '''
            SELECT * FROM categories
            WHERE category_id = %s
        '''
    cursor.execute(query, (product['category_id'],))
    category = cursor.fetchone()

    cursor.close()
    connection.close()

    if not product:
        return jsonify({"error": "Product not found."}), 404

    return render_template('vendor_edit.html', product=product, category=category)


@vendor_view.route('/delete_product', methods=['POST'])
def delete_product():
    product_id = request.form.get('product_id')
    if not product_id:
        return jsonify({"error": "No product ID provided."}), 400
    print(product_id)

    # connect to database
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # delete product from products table
    query = '''
        DELETE FROM products
        WHERE product_id = %s
    '''
    cursor.execute(query, (product_id,))

    # submit changes
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"status": "success"}), 200


@vendor_view.route('/update_product', methods=['POST'])
def update_product():
    if request.method == 'POST':
        if session.get('user_type') == 'vendor':
            vendor_id = session.get('user_id')
        else:
            return redirect(url_for('login.login_page'))

        original_image = request.form.get('original_image')

        # check if a new image has been uploaded
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

            # save file to root path
            file.save(save_path)

            new_filename = current_app.config['UPLOAD_PRODUCT'] + '/' + new_filename

        # If no new files have been uploaded, the URL of the original image is used
        if not new_filename:
            new_filename = original_image

        # Process additional form data and save product data to the database
        product_id = request.form['product_id']
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
            now = datetime.now()
            query = """
                UPDATE products SET
            category_id = %s, name = %s, description = %s, price= %s, 
            stock= %s, picture=%s, promotion=%s, duration_start=%s, duration_end=%s, product_status=%s, release_date=%s 
            where product_id = %s
            """
            cursor.execute(query, (
                category_id, name, description, price, stock, new_filename, promotion, duration_start,
                duration_end, product_status, now, product_id))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('vendor_view.view_page'))

        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return redirect(request.url)
