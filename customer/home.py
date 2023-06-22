from datetime import datetime

import mysql.connector
from db_config import db_connection
from flask import jsonify, request, render_template, Blueprint

home = Blueprint('home', __name__)


# try to format time in different situations
def format_time_diff(time_diff):
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days == 1:
        return f"{days} day"
    elif days > 1:
        return f"{days} days"
    elif hours == 1:
        return f"{hours} hour"
    elif hours > 1:
        return f"{hours} hours"
    elif minutes == 1:
        return f"{minutes} minute"
    elif minutes > 1:
        return f"{minutes} minutes"
    else:
        return f"{seconds} s"


# try to gwt thw categories from database
@home.route('/home_page')
def home_page():
    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM categories WHERE level IN (1, 2)")
        categories = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        categories = [dict(zip(column_names, row)) for row in categories]
    except mysql.connector.Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

    return render_template('home.html', categories=categories)


# try to get the products from database
@home.route('/products', methods=['GET'])
def products():
    per_page = 6
    last_date = request.args.get('last_date', None)
    last_id = request.args.get('last_id', None, type=int)
    category_id = request.args.get('category_id', None, type=int)  # 获取 category_id 参数

    if last_date:
        last_date = datetime.strptime(last_date, '%a, %d %b %Y %H:%M:%S %Z')

    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.release_date, p.product_id, p.picture "
                 "FROM products p LEFT JOIN vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' "
                 "AND (p.release_date < %s OR (p.release_date = %s AND p.product_id < %s) OR %s IS NULL) "
                 "AND (%s IS NULL OR p.category_id = %s) "
                 "ORDER BY p.release_date DESC, p.product_id DESC LIMIT %s")
        cursor.execute(query, (last_date, last_date, last_id, last_date, category_id, category_id, per_page))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()
        for product in products:
            release_date = product['release_date'].replace(tzinfo=None)  # remove time zone information
            time_diff = current_time - release_date
            product['time_diff'] = format_time_diff(time_diff)
    finally:
        cursor.close()
        conn.close()

    return jsonify(products)


# try to get the recently commented products from database
@home.route('/comments', methods=['GET'])
def comments():
    per_page = 7
    last_date = request.args.get('last_date', None)
    last_id = request.args.get('last_id', None, type=int)
    category_id = request.args.get('category_id', None, type=int)

    if last_date:
        last_date = datetime.strptime(last_date, '%a, %d %b %Y %H:%M:%S %Z')

    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.last_comment, p.product_id, p.picture "
                 "FROM products p LEFT JOIN vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' "
                 "AND (p.last_comment < %s OR (p.last_comment = %s AND p.product_id < %s) OR %s IS NULL) "
                 "AND (%s IS NULL OR p.category_id = %s) "
                 "ORDER BY p.last_comment DESC, p.product_id DESC LIMIT %s")
        cursor.execute(query, (last_date, last_date, last_id, last_date, category_id, category_id, per_page))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()

        # for product in products:
        #     release_date = product['last_comment'].replace(tzinfo=None)
        #     time_diff = current_time - release_date
        #     product['time_diff'] = format_time_diff(time_diff)

        # if product['last_comment'] is not None:
        filtered_products = []
        for product in products:
            if product['last_comment'] is not None:
                release_date = product['last_comment'].replace(tzinfo=None)
                time_diff = current_time - release_date
                product['time_diff'] = format_time_diff(time_diff)
                filtered_products.append(product)
            else:
                pass
    finally:
        cursor.close()
        conn.close()

    return jsonify(filtered_products)


# try to get the recently liked products from database
@home.route('/likes', methods=['GET'])
def likes():
    per_page = 8
    last_date = request.args.get('last_date', None)
    last_id = request.args.get('last_id', None, type=int)
    category_id = request.args.get('category_id', None, type=int)

    if last_date:
        last_date = datetime.strptime(last_date, '%a, %d %b %Y %H:%M:%S %Z')

    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.last_like_dis, p.product_id, p.picture "
                 "FROM products p LEFT JOIN vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' "
                 "AND (p.last_like_dis < %s OR (p.last_like_dis = %s AND p.product_id < %s) OR %s IS NULL) "
                 "AND (%s IS NULL OR p.category_id = %s) "
                 "ORDER BY p.last_like_dis DESC, p.product_id DESC LIMIT %s")
        cursor.execute(query, (last_date, last_date, last_id, last_date, category_id, category_id, per_page))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()
        # for product in products:
        #     release_date = product['last_like_dis'].replace(tzinfo=None)
        #     time_diff = current_time - release_date
        #     product['time_diff'] = format_time_diff(time_diff)

        filtered_products = []

        # if product['last_like_dis'] is not None:
        for product in products:
            if product['last_like_dis'] is not None:
                release_date = product['last_like_dis'].replace(tzinfo=None)
                time_diff = current_time - release_date
                product['time_diff'] = format_time_diff(time_diff)
                filtered_products.append(product)
            else:
                pass

    finally:
        cursor.close()
        conn.close()

    return jsonify(filtered_products)


# try to get the searched products from database
@home.route('/search_products', methods=['GET'])
def search_products():
    search_query = request.args.get('query', '')
    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.release_date, p.product_id, p.picture "
                 "FROM products p left join vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' AND "
                 "(p.name LIKE %s OR v.vendor_name LIKE %s OR p.price LIKE %s) "
                 "ORDER BY p.release_date DESC, p.product_id DESC")
        search_param = f"%{search_query}%"
        cursor.execute(query, (search_param, search_param, search_param))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()
        for product in products:
            release_date = product['release_date'].replace(tzinfo=None)
            time_diff = current_time - release_date
            product['time_diff'] = format_time_diff(time_diff)
    finally:
        cursor.close()
        conn.close()

    return jsonify(products)


# try to get the searched comments from database
@home.route('/search_comments', methods=['GET'])
def search_comments():
    search_query = request.args.get('query', '')
    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.last_comment, p.product_id, p.picture "
                 "FROM products p left join vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' AND "
                 "(p.name LIKE %s OR v.vendor_name LIKE %s OR p.price LIKE %s) "
                 "ORDER BY p.last_comment DESC, p.product_id DESC")
        search_param = f"%{search_query}%"
        cursor.execute(query, (search_param, search_param, search_param))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()
        # for product in products:
        #     release_date = product['last_comment'].replace(tzinfo=None)
        #     time_diff = current_time - release_date
        #     product['time_diff'] = format_time_diff(time_diff)

        filtered_products = []
        for product in products:
            if product['last_comment'] is not None:
                release_date = product['last_comment'].replace(tzinfo=None)
                time_diff = current_time - release_date
                product['time_diff'] = format_time_diff(time_diff)
                filtered_products.append(product)
            else:
                pass
    finally:
        cursor.close()
        conn.close()

    return jsonify(filtered_products)


# try to get the searched likes from database
@home.route('/search_likes', methods=['GET'])
def search_likes():
    search_query = request.args.get('query', '')
    conn = mysql.connector.connect(**db_connection)
    cursor = conn.cursor()

    try:
        query = ("SELECT p.name, p.price, v.vendor_name, p.last_like_dis, p.product_id, p.picture "
                 "FROM products p LEFT JOIN vendors v ON p.vendor_id = v.vendor_id "
                 "WHERE p.product_status = 'active' AND "
                 "(p.name LIKE %s OR v.vendor_name LIKE %s OR p.price LIKE %s) "
                 "ORDER BY p.last_like_dis DESC, p.product_id DESC")
        search_param = f"%{search_query}%"
        cursor.execute(query, (search_param, search_param, search_param))

        products = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]
        products = [dict(zip(column_names, row)) for row in products]

        current_time = datetime.now()
        # for product in products:
        #     release_date = product['last_like_dis'].replace(tzinfo=None)
        #     time_diff = current_time - release_date
        #     product['time_diff'] = format_time_diff(time_diff)
        filtered_products = []
        for product in products:
            if product['last_like_dis'] is not None:
                release_date = product['last_like_dis'].replace(tzinfo=None)
                time_diff = current_time - release_date
                product['time_diff'] = format_time_diff(time_diff)
                filtered_products.append(product)
            else:
                pass

    finally:
        cursor.close()
        conn.close()

    return jsonify(filtered_products)
