import mysql.connector
from db_config import db_connection
from flask import Blueprint, session, redirect, url_for, render_template, request

order = Blueprint('order', __name__)


# display all orders
@order.route('/order_page', methods=['GET', 'POST'])
def order_page():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # query_orders = '''
    #     SELECT o.order_id, o.product_id, o.quantity, o.total_amount, py.payment_status,
    #     o.payment_id, p.name, p.description, p.price, p.picture,
    #     p.category_id, o.order_time, v.vendor_name, o.status, o.delivery_time, a.content, py.finish_time
    #     FROM orders o
    #     LEFT JOIN products p ON o.product_id = p.product_id
    #     LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
    #     LEFT JOIN payment py ON o.payment_id = py.payment_id
    #     LEFT JOIN announcements a ON o.order_id = a.order_id
    #     WHERE o.customer_id = %s
    #     ORDER BY o.order_time DESC
    # '''

    query_orders = '''
            SELECT o.order_id, o.product_id, o.quantity, o.total_amount, py.payment_status, 
            o.payment_id, p.name, p.description, p.price, p.picture, 
            p.category_id, o.order_time, v.vendor_name, o.status, o.delivery_time, a.content, py.finish_time
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.product_id
            LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
            LEFT JOIN payment py ON o.payment_id = py.payment_id
            LEFT JOIN 
                (SELECT order_id, MAX(announcement_date) as MaxTime
                 FROM announcements
                 GROUP BY order_id) a1 ON o.order_id = a1.order_id
            LEFT JOIN 
                announcements a ON a.order_id = a1.order_id AND a.announcement_date = a1.MaxTime
            WHERE o.customer_id = %s
            ORDER BY o.order_time DESC
        '''
    cursor.execute(query_orders, (customer_id,))
    order_rows = cursor.fetchall()

    # group for payment_id
    orders_data = {}
    for row in order_rows:
        payment_id = row[5]
        if payment_id not in orders_data:
            orders_data[payment_id] = []

        order_item = {
            'order_id': row[0],
            'product_id': row[1],
            'quantity': row[2],
            'total_amount': row[3],
            'status': row[4],
            'product_name': row[6],
            'product_description': row[7],
            'product_price': row[8],
            'product_image': row[9],
            'product_category': row[10],
            'order_time': row[11],
            'vendor_name': row[12],
            'order_status': row[13],
            'delivery_time': row[14],
            'announcement': row[15],
            'finish_time': row[16],
        }
        orders_data[payment_id].append(order_item)

    return render_template('order.html', orders_data=orders_data)


#  display order which status is the corresponding status
@order.route('/filter_order_status', methods=['GET'])
def filter_order_status():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    status = request.args.get('status')

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # query_orders = '''
    #     SELECT o.order_id, o.product_id, o.quantity, o.total_amount, py.payment_status,
    #     o.payment_id, p.name, p.description, p.price, p.picture,
    #     p.category_id, o.order_time, v.vendor_name, o.status, o.delivery_time, a.content, py.finish_time
    #     FROM orders o
    #     LEFT JOIN products p ON o.product_id = p.product_id
    #     LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
    #     LEFT JOIN payment py ON o.payment_id = py.payment_id
    #     LEFT JOIN announcements a ON o.order_id = a.order_id
    #     WHERE o.customer_id = %s
    # '''

    query_orders = '''
            SELECT o.order_id, o.product_id, o.quantity, o.total_amount, py.payment_status, 
            o.payment_id, p.name, p.description, p.price, p.picture, 
            p.category_id, o.order_time, v.vendor_name, o.status, o.delivery_time, a.content, py.finish_time
            FROM orders o
            LEFT JOIN products p ON o.product_id = p.product_id
            LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
            LEFT JOIN payment py ON o.payment_id = py.payment_id
            LEFT JOIN 
                (SELECT order_id, MAX(announcement_date) as MaxTime
                 FROM announcements
                 GROUP BY order_id) a1 ON o.order_id = a1.order_id
            LEFT JOIN 
                announcements a ON a.order_id = a1.order_id AND a.announcement_date = a1.MaxTime
            WHERE o.customer_id = %s
        '''
    if status != "all":
        query_orders += "AND o.status = %s ORDER BY o.order_time DESC"
        cursor.execute(query_orders, (customer_id, status))
    else:
        query_orders += "ORDER BY o.order_time DESC"
        cursor.execute(query_orders, (customer_id,))
    order_rows = cursor.fetchall()

    orders_data = {}
    for row in order_rows:
        payment_id = row[5]
        if payment_id not in orders_data:
            orders_data[payment_id] = []

        order_item = {
            'order_id': row[0],
            'product_id': row[1],
            'quantity': row[2],
            'total_amount': row[3],
            'status': row[4],
            'product_name': row[6],
            'product_description': row[7],
            'product_price': row[8],
            'product_image': row[9],
            'product_category': row[10],
            'order_time': row[11],
            'vendor_name': row[12],
            'order_status': row[13],
            'delivery_time': row[14],
            'announcement': row[15],
            'finish_time': row[16],
        }
        orders_data[payment_id].append(order_item)

    return render_template('order.html', orders_data=orders_data)
