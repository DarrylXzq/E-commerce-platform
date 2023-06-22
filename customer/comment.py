from datetime import datetime

import mysql.connector
from db_config import db_connection
from flask import render_template, Blueprint, request, jsonify, session, redirect, url_for

comment = Blueprint('comment', __name__)


# try to get the comment page of a product
@comment.route('/comment_page/<int:product_id>')
def comment_page(product_id):
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = """
            SELECT p.name, p.description, p.picture, v.vendor_name, p.product_id
            FROM products AS p
            LEFT JOIN vendors AS v ON p.vendor_id = v.vendor_id
            WHERE p.product_id = %s
        """
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    filename = result[2].replace("../static/", "")

    if result:
        product = {
            "name": result[0],
            "description": result[1],
            "picture": filename,
            "vendor_name": result[3],
            "product_id": result[4]
        }
    else:
        product = None

    query = """
        SELECT co.comment_date, co.comment, cu.avatar, cu.name
        FROM comments as co
        LEFT JOIN customers as cu ON co.customer_id = cu.customer_id
        WHERE co.product_id = %s AND co.customer_id = %s
        ORDER BY co.comment_date DESC
    """
    cursor.execute(query, (product_id, customer_id))

    results = cursor.fetchall()
    comments = []
    if results:
        for result in results:
            path = result[2]
            if "../static/" in path:
                filename = path.replace("../static/", "")
            elif "static/" in path:
                filename = path.replace("static", "").replace("\\", "/").strip("/")
            comment = {
                "date": result[0],
                "text": result[1],
                "avatar": filename,
                "customer": result[3]
            }
            comments.append(comment)

    cursor.close()
    connection.close()

    return render_template('comment.html', product=product, comments=comments)


# try to submit a comment
@comment.route('/comment_submit', methods=['POST'])
def comment_submit():
    data = request.get_json()
    product_id = data.get('product_id')
    comment = data.get('comment')
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    # verify the data
    if not product_id or not comment:
        return jsonify(success=False, message='Invalid data')

    # update the price
    now = datetime.now()
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()
    query = """
            INSERT INTO comments (customer_id, product_id, comment, comment_date)
            VALUES (%s, %s, %s, %s)
        """

    cursor.execute(query, (customer_id, product_id, comment, now))
    connection.commit()

    # =====================================================================
    # update the product table
    query = """
        UPDATE products SET last_comment = %s WHERE product_id = %s
    """
    cursor.execute(query, (now, product_id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify(success=True, message='Comment submitted successfully')


# try to get all comments that a customer has made
@comment.route('/review/<int:last_product>')
def review(last_product):
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT product_id, MAX(comment_date) AS latest_comment_date
        FROM comments
        WHERE customer_id = %s
        GROUP BY product_id
        ORDER BY latest_comment_date DESC
    """, (customer_id,))

    product_ids = [result[0] for result in cursor.fetchall()]

    cursor.execute("""
        SELECT p.product_id, p.name, p.description, v.vendor_name, p.picture
        FROM products p
        LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        WHERE p.product_id IN ({})
    """.format(', '.join(['%s'] * len(product_ids))), tuple(product_ids))

    fetched_products = [{
        'product_id': product_id,
        'name': name,
        'description': description,
        'vendor_name': vendor_name,
        'picture': picture
    } for product_id, name, description, vendor_name, picture in cursor.fetchall()]

    products = sorted(fetched_products, key=lambda x: product_ids.index(x['product_id']))

    cursor.close()
    connection.close()

    return render_template('all_comments.html', products=products, last_product=last_product)
