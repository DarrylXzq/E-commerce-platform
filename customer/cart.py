from datetime import datetime

# try to import mysql.connector and the basic flask modules
import mysql.connector
from db_config import db_connection
from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template

cart = Blueprint('cart', __name__)


#  try to delete an item from the cart
def delete_item_from_cart(cart_id):
    try:
        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        query = "DELETE FROM carts WHERE cart_id = %s"
        cursor.execute(query, (cart_id,))

        connection.commit()
        cursor.close()
        connection.close()

        return True, "Item deleted successfully"
    except Exception as e:
        return False, str(e)


# try to render the cart page
@cart.route('/cart_page')
def cart_page():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query = '''
        SELECT c.cart_id, c.product_id, c.quantity, 
        c.add_time, p.name, p.description, p.price, p.promotion, p.picture, p.stock, c.selected, v.vendor_name, p.duration_start, p.duration_end
        FROM carts c
        LEFT JOIN products p ON c.product_id = p.product_id
        LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        WHERE c.customer_id = %s
        ORDER BY c.add_time DESC
    '''
    cursor.execute(query, (customer_id,))
    cart_items = cursor.fetchall()
    # try to make the time format consistent
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    cart_products = []
    for item in cart_items:
        cart_products.append({
            'cart_id': item[0],
            'product_id': item[1],
            'quantity': item[2],
            'add_time': item[3],
            'name': item[4],
            'description': item[5],
            'price': item[6],
            'promotion': item[7],
            'picture': item[8],
            'stock': item[9],
            'selected': item[10],
            'vendor_name': item[11],
            'duration_start': item[12].strftime('%Y-%m-%dT%H:%M:%S') if item[12] else None,
            'duration_end': item[13].strftime('%Y-%m-%dT%H:%M:%S') if item[13] else None,
            'now': now
        })

    return render_template('cart.html', cart_products=cart_products)


# try to add an item to the cart
@cart.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    quantity = int(request.form.get('quantity'))
    # price = float(request.form.get('price'))

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()
    now = datetime.now()

    query = """
            SELECT cart_id, quantity
            FROM carts
            WHERE customer_id = %s AND product_id = %s
        """

    cursor.execute(query, (customer_id, product_id))
    result = cursor.fetchone()

    if result:
        # check if the product already exists in the cart
        cart_id, current_quantity = result
        new_quantity = current_quantity + quantity

        query = """
                UPDATE carts
                SET quantity = %s, add_time = %s
                WHERE cart_id = %s
            """

        cursor.execute(query, (new_quantity, now, cart_id))

    else:
        # if the product does not exist in the cart
        query = """
                INSERT INTO carts (customer_id, product_id, quantity, add_time)
                VALUES (%s, %s, %s, %s)
            """

        cursor.execute(query, (customer_id, product_id, quantity, now))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(success=True, message='Added to cart successfully')


# try to delete an item from the cart
@cart.route('/delete_item', methods=['POST'])
def delete_item():
    cart_id = request.form.get('cart_id')
    success, message = delete_item_from_cart(cart_id)
    if success:
        return jsonify({'success': True, 'message': 'Item deleted successfully'})
    else:
        return jsonify({'success': False, 'message': message})


# try to update the quantity of an item in the cart
@cart.route('/update_cart_item', methods=['POST'])
def update_cart_item():
    cart_id = request.form.get('cart_id')
    new_quantity = request.form.get('quantity')

    try:
        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        query = "UPDATE carts SET quantity = %s WHERE cart_id = %s"
        cursor.execute(query, (new_quantity, cart_id))

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': 'Item updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# try to update the selected status of an item in the cart
@cart.route('/update_selected', methods=['POST'])
def update_selected():
    cart_id = request.form.get('cart_id')
    selected = request.form.get('selected')

    selected_int = 1 if selected.lower() == 'true' else 0

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE carts
        SET selected = %s
        WHERE cart_id = %s
    """, (selected_int, cart_id))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({'status': 'success'})
