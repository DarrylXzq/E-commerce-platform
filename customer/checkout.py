import datetime

import mysql.connector
from db_config import db_connection
from flask import Blueprint, session, redirect, url_for, render_template, request, jsonify

checkout = Blueprint('checkout', __name__)


# show the checkout page
@checkout.route('/checkout_page', methods=['GET', 'POST'])
def checkout_page():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    total_price = None
    discounted_price = None
    new_cart_items = []
    payment_id = None

    if request.method == 'POST':
        total_price = request.form.get('total_price', None)
        discounted_price = request.form.get('discounted_price')

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # get the address information
    query = '''
        SELECT country_name, province_name, city_name, address, receiver_name, receiver_phone, address_id
        FROM addresses_customer
        WHERE customer_id = %s
    '''
    cursor.execute(query, (customer_id,))
    address_rows = cursor.fetchall()

    # get the chose address information
    query = '''
        SELECT p.product_id, p.name, v.vendor_name, p.description, p.price, p.promotion, p.duration_start, p.duration_end, c.quantity, p.picture
        FROM carts c
        LEFT JOIN products p ON c.product_id = p.product_id
        LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        WHERE c.customer_id = %s AND c.selected = 1
    '''
    cursor.execute(query, (customer_id,))
    cart_items = cursor.fetchall()

    if request.method == 'POST':
        # create new payment
        query = '''
            INSERT INTO payment (payment_date, payment_status)
            VALUES (NOW(), 'pending')
        '''
        cursor.execute(query)
        connection.commit()
        payment_id = cursor.lastrowid

        # insert into orders
        for item in cart_items:
            product_id, product_name, seller_name, product_description, product_price, product_promotion, duration_start, duration_end, quantity, picture = item

            # check if the product is still in promotion
            current_time = datetime.datetime.now()
            if duration_start <= current_time <= duration_end:
                final_price = (100 - product_promotion) / 100 * product_price
            else:
                final_price = product_price

            total_amount = final_price * quantity

            item_list = list(item)
            item_list.append(total_amount)
            new_item = tuple(item_list)
            new_cart_items.append(new_item)

            query = '''
                INSERT INTO orders (customer_id, product_id, quantity, total_amount, payment_id, address_id, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'pending')
            '''
            if not address_rows:
                return redirect(url_for('nav_user.mail_info'))
            else:
                cursor.execute(query, (customer_id, product_id, quantity, total_amount, payment_id, address_rows[0][6]))
            connection.commit()

            # update stock
            update_query = '''
                UPDATE products
                SET stock = stock - %s
                WHERE product_id = %s
            '''
            cursor.execute(update_query, (quantity, product_id))
            connection.commit()
    index = 0
    address_strings = []
    for row in address_rows:
        index += 1
        address_info = {
            "address_str": f"{index}: Country: {row[0]}, Province: {row[1]}, City: {row[2]}, Address: {row[3]}, Receiver:{row[4]}, Receiver_phone: {row[5]}",
            "address_id": row[6]
        }
        address_strings.append(address_info)

    return render_template('check_out.html', address_strings=address_strings, cart_items=new_cart_items,
                           total_price=total_price, discounted_price=discounted_price, payment_id=payment_id)


@checkout.route('/repay_page', methods=['GET', 'POST'])
def repay_page():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    total_price = 0
    new_cart_items = []
    payment_id = None

    if request.method == 'POST':
        payment_id = request.form.get('payment_id')

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # get the address information
    query = '''
        SELECT country_name, province_name, city_name, address, receiver_name, receiver_phone, address_id
        FROM addresses_customer
        WHERE customer_id = %s
    '''
    cursor.execute(query, (customer_id,))
    address_rows = cursor.fetchall()

    # get the chose address information
    query = '''
        SELECT p.product_id, p.name, v.vendor_name, p.description, p.price, p.promotion, p.duration_start, p.duration_end, c.quantity, p.picture
        FROM carts c
        LEFT JOIN products p ON c.product_id = p.product_id
        LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        LEFT JOIN orders o ON c.product_id = o.product_id
        LEFT JOIN payment py ON o.payment_id = py.payment_id
        WHERE c.customer_id = %s AND py.payment_id = %s
    '''
    cursor.execute(query, (customer_id, payment_id))
    cart_items = cursor.fetchall()

    # insert into orders
    for item in cart_items:
        product_id, product_name, seller_name, product_description, product_price, product_promotion, duration_start, duration_end, quantity, picture = item

        # check if the product is still in promotion
        current_time = datetime.datetime.now()
        if duration_start <= current_time <= duration_end:
            final_price = (100 - product_promotion) / 100 * product_price
        else:
            final_price = product_price

        total_amount = final_price * quantity

        total_price += product_price * quantity

        item_list = list(item)
        item_list.append(total_amount)
        new_item = tuple(item_list)
        new_cart_items.append(new_item)

    query_orders = '''
            SELECT total_amount
            FROM orders
            WHERE payment_id = %s
        '''
    cursor.execute(query_orders, (payment_id,))
    order_rows = cursor.fetchall()

    # receive the total amount
    total_amount = sum(row[0] for row in order_rows)
    discounted_price = str(total_amount)

    index = 0
    address_strings = []
    for row in address_rows:
        index += 1
        address_info = {
            "address_str": f"{index}: Country: {row[0]}, Province: {row[1]}, City: {row[2]}, Address: {row[3]}, Receiver:{row[4]}, Receiver_phone: {row[5]}",
            "address_id": row[6]
        }
        address_strings.append(address_info)

    return render_template('check_out.html', address_strings=address_strings, cart_items=new_cart_items,
                           total_price=total_price, discounted_price=discounted_price, payment_id=payment_id)


# when the user choose the address, update the address_id in the orders table
@checkout.route('/update_address_id', methods=['POST'])
def update_address_id():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))
    address_id = request.form.get('address_id')
    payment_id = request.form.get('payment_id')
    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    # 更新数据库中的 address_id
    query = '''
        UPDATE orders
        SET address_id = %s
        WHERE customer_id = %s AND payment_id = %s
    '''
    cursor.execute(query, (address_id, customer_id, payment_id))
    connection.commit()

    return jsonify({'message': 'Address updated successfully'})


# click the cancel button, cancel the order
@checkout.route('/cancel_order', methods=['POST'])
def cancel_order():
    payment_id = request.form.get('payment_id')

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    try:
        # Get all the products and quantities related to the cancelled order
        get_order_items_query = "SELECT product_id, quantity FROM orders WHERE payment_id = %s"
        cursor.execute(get_order_items_query, (payment_id,))
        order_items = cursor.fetchall()

        # Update the product stocks
        for product_id, quantity in order_items:
            update_product_stock_query = "UPDATE products SET stock = stock + %s WHERE product_id = %s"
            cursor.execute(update_product_stock_query, (quantity, product_id))
            connection.commit()

        update_orders_query = "UPDATE orders SET status = 'cancelled' WHERE payment_id = %s"
        cursor.execute(update_orders_query, (payment_id,))
        connection.commit()

        # Update payments table status to 'cancelled'
        update_payments_query = "UPDATE payment SET payment_status = 'cancelled' WHERE payment_id = %s"
        cursor.execute(update_payments_query, (payment_id,))
        connection.commit()

        # Close the database connection
        cursor.close()
        connection.close()
        return jsonify(status="success")
    except Exception as e:
        # If there was an error during the update, return an error status
        print(e)
        return jsonify(status="error")
