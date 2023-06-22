import mysql.connector
from db_config import db_connection
from flask import Blueprint, render_template, session, redirect, url_for, request

vendor_order = Blueprint('vendor_order', __name__)


# order view page
@vendor_order.route('/order_view')
def order_view():
    if session.get('user_type') == 'vendor':
        vendor_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # query = """
    #     SELECT o.order_id, py.payment_id, py.payment_status, py.payment_date, py.finish_time,
    #     o.product_id, o.quantity, o.total_amount, o.status, o.delivery_time, a.content,
    #     p.name, p.description, p.price, p.picture, p.category_id, v.vendor_name
    #     FROM orders o
    #     LEFT JOIN payment py ON o.payment_id = py.payment_id
    #     LEFT JOIN products p ON o.product_id = p.product_id
    #     LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
    #     LEFT JOIN announcements a ON o.order_id = a.order_id
    #     WHERE v.vendor_id = %s AND py.payment_status = 'paid'
    #     ORDER BY py.finish_time DESC
    # """

    query = """
            SELECT o.order_id, py.payment_id, py.payment_status, py.payment_date, py.finish_time, 
            o.product_id, o.quantity, o.total_amount, o.status, o.delivery_time, a.content,
            p.name, p.description, p.price, p.picture, p.category_id, v.vendor_name
            FROM orders o
            LEFT JOIN payment py ON o.payment_id = py.payment_id 
            LEFT JOIN products p ON o.product_id = p.product_id
            LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
            LEFT JOIN 
                (SELECT order_id, MAX(announcement_date) as MaxTime
                 FROM announcements
                 GROUP BY order_id) a1 ON o.order_id = a1.order_id
            LEFT JOIN 
                announcements a ON a.order_id = a1.order_id AND a.announcement_date = a1.MaxTime
            WHERE v.vendor_id = %s AND py.payment_status = 'paid' 
            ORDER BY py.finish_time DESC
    """
    cursor.execute(query, (vendor_id,))

    order_rows = cursor.fetchall()
    orders_data = []
    for row in order_rows:
        order_item = {
            'order_id': row[0],
            'payment_id': row[1],
            'payment_status': row[2],
            'payment_time': row[3],
            'finish_time': row[4],
            'product_id': row[5],
            'quantity': row[6],
            'total_amount': row[7],
            'order_status': row[8],
            'delivery_time': row[9],
            'announcement': row[10],
            'product_name': row[11],
            'product_description': row[12],
            'product_price': row[13],
            'product_image': row[14],
            'product_category': row[15],
            'vendor_name': row[16],
        }
        orders_data.append(order_item)

    return render_template('vendor_order.html', orders_data=orders_data)


# display order detail which in corresponding status
@vendor_order.route('/filter_order_status', methods=['GET'])
def filter_order_status():
    if session.get('user_type') == 'vendor':
        vendor_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    status = request.args.get('status')

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # query_orders = """
    #         SELECT o.order_id, py.payment_id, py.payment_status, py.payment_date, py.finish_time,
    #         o.product_id, o.quantity, o.total_amount, o.status, o.delivery_time, a.content,
    #         p.name, p.description, p.price, p.picture, p.category_id, v.vendor_name
    #         FROM orders o
    #         LEFT JOIN payment py ON o.payment_id = py.payment_id
    #         LEFT JOIN products p ON o.product_id = p.product_id
    #         LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
    #         LEFT JOIN announcements a ON o.order_id = a.order_id
    #         WHERE v.vendor_id = %s AND py.payment_status = 'paid'
    #     """

    query_orders = """
                SELECT o.order_id, py.payment_id, py.payment_status, py.payment_date, py.finish_time, 
                o.product_id, o.quantity, o.total_amount, o.status, o.delivery_time, a.content,
                p.name, p.description, p.price, p.picture, p.category_id, v.vendor_name
                FROM orders o
                LEFT JOIN payment py ON o.payment_id = py.payment_id 
                LEFT JOIN products p ON o.product_id = p.product_id
                LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
                LEFT JOIN 
                    (SELECT order_id, MAX(announcement_date) as MaxTime
                     FROM announcements
                     GROUP BY order_id) a1 ON o.order_id = a1.order_id
                LEFT JOIN 
                    announcements a ON a.order_id = a1.order_id AND a.announcement_date = a1.MaxTime
                WHERE v.vendor_id = %s AND py.payment_status = 'paid' 
            """

    if status != "all":
        query_orders += "AND o.status = %s ORDER BY py.finish_time DESC"
        cursor.execute(query_orders, (vendor_id, status))
    else:
        query_orders += "ORDER BY o.order_time DESC"
        cursor.execute(query_orders, (vendor_id,))

    order_rows = cursor.fetchall()
    orders_data = []
    for row in order_rows:
        order_item = {
            'order_id': row[0],
            'payment_id': row[1],
            'payment_status': row[2],
            'payment_time': row[3],
            'finish_time': row[4],
            'product_id': row[5],
            'quantity': row[6],
            'total_amount': row[7],
            'order_status': row[8],
            'delivery_time': row[9],
            'announcement': row[10],
            'product_name': row[11],
            'product_description': row[12],
            'product_price': row[13],
            'product_image': row[14],
            'product_category': row[15],
            'vendor_name': row[16],
        }
        orders_data.append(order_item)

    return render_template('vendor_order.html', orders_data=orders_data)
