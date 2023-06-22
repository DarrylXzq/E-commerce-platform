from datetime import datetime

import mysql.connector
from db_config import db_connection
from flask import render_template, Blueprint, request, jsonify, session, redirect, url_for

detail = Blueprint('detail', __name__)


# try to get product detail
@detail.route('/detail_page/<int:product_id>')
def detail_page(product_id):
    now = datetime.now()
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = """
        SELECT p.name, p.description, p.price, p.stock, p.picture, v.vendor_name, 
        v.email, v.phone, p.promotion, p.duration_start, p.duration_end, p.likes, p.dislikes, p.product_id,v.vendor_id
        FROM products AS p
        LEFT JOIN vendors AS v ON p.vendor_id = v.vendor_id
        WHERE p.product_id = %s
    """
    cursor.execute(query, (product_id,))
    result = cursor.fetchone()
    filename = result[4].replace("../static/", "")

    if result:
        product = {
            "name": result[0],
            "description": result[1],
            "price": result[2],
            "stock": result[3],
            "picture": filename,
            "vendor_name": result[5],
            "vendor_email": result[6],
            "vendor_phone": result[7],
            "discount": result[8],
            "duration_start": result[9],
            "duration_end": result[10],
            "likes": result[11],
            "dislikes": result[12],
            "product_id": result[13],
            "vendor_id": result[14]
        }
    else:
        product = None

    cursor.close()
    connection.close()

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = "SELECT co.comment_date, co.comment, cu.avatar, cu.name FROM comments as co " \
            "LEFT JOIN customers as cu ON co.customer_id = cu.customer_id  WHERE product_id = %s ORDER BY comment_date DESC"
    cursor.execute(query, (product_id,))
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

    return render_template('product_detail.html', product=product, comments=comments, now=now)


# update the likes and dislikes ,when the user click the like or dislike button
@detail.route('/update_likes_dislikes', methods=['POST'])
def update_likes_dislikes():
    data = request.get_json()
    product_id = data.get('product_id')
    action = data.get('action')
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    # verify data
    if not product_id or not action:
        return jsonify(success=False, message='Invalid data')

    # update favorites table
    now = datetime.now()
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()
    query = """
            INSERT INTO favorites (customer_id, product_id, like_button, dislike_button, favorite_date)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                like_button = VALUES(like_button),
                dislike_button = VALUES(dislike_button),
                favorite_date = VALUES(favorite_date)
        """

    cursor.execute(query, (customer_id, product_id, action == 'like', action == 'dislike', now))
    connection.commit()

    # =====================================================================
    # update products table
    query = """
        UPDATE products
        SET likes = (
            SELECT COUNT(*) FROM favorites WHERE product_id = %s AND like_button = TRUE
        ),
        dislikes = (
            SELECT COUNT(*) FROM favorites WHERE product_id = %s AND dislike_button = TRUE
        ),
        last_like_dis = %s
        WHERE product_id = %s
    """
    cursor.execute(query, (product_id, product_id, now, product_id))
    connection.commit()

    # get updated likes and dislikes
    cursor.execute(
        "SELECT likes, dislikes, like_button, dislike_button "
        "FROM products p LEFT JOIN favorites f ON p.product_id = f.product_id AND f.customer_id = %s WHERE p.product_id = %s",
        (customer_id, product_id))
    result = cursor.fetchone()
    likes, dislikes, user_like_status, user_dislike_status = result

    cursor.close()
    connection.close()

    return jsonify(success=True, likes=likes, dislikes=dislikes, user_like_status=user_like_status,
                   user_dislike_status=user_dislike_status)


# display the like and dislike button
@detail.route('/display_like/<int:product_id>', methods=['GET'])
def display_like(product_id):
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT like_button, dislike_button "
        "FROM favorites WHERE product_id = %s AND customer_id = %s",
        (product_id, customer_id))
    result = cursor.fetchone()

    if result:
        user_like_status, user_dislike_status = result
    else:
        user_like_status, user_dislike_status = False, False

    cursor.close()
    connection.close()

    return jsonify(success=True, user_like_status=user_like_status, user_dislike_status=user_dislike_status)


# display the all products of the vendor
@detail.route('/vendor_page/<int:vendor_id>')
def vendor_page(vendor_id):
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT p.product_id, p.name, p.description, v.vendor_name, p.picture
        FROM products p
        LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        WHERE v.vendor_id = %s
        order by p.release_date desc
    """, (vendor_id,))

    fetched_products = [{
        'product_id': product_id,
        'name': name,
        'description': description,
        'vendor_name': vendor_name,
        'picture': picture,
        'vendor_id': vendor_id
    } for product_id, name, description, vendor_name, picture in cursor.fetchall()]

    cursor.close()
    connection.close()

    return render_template('all_products.html', products=fetched_products, vendor_id=vendor_id)
