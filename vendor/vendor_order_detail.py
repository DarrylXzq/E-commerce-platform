import mysql.connector
from db_config import db_connection
from flask import Blueprint, render_template, request, session, redirect, url_for

vendor_order_detail = Blueprint('vendor_order_detail', __name__)


# to find the order detail of a specific order
@vendor_order_detail.route('/vendor_order_detail_page', methods=['GET', 'POST'])
def vendor_order_detail_page():
    if session.get('user_type') == 'vendor':
        vendor_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))

    if request.method == 'POST':
        order_id = request.form.get('order_id')

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        # query = '''
        #     SELECT v.vendor_name, v.email as vendor_email, v.phone as vendor_phone, c.name as customer_name, c.email as customer_email,
        #            c.phone as customer_phone, ac.country_name as customer_country, ac.province_name as customer_province,
        #             ac.city_name as customer_city, ac.address as customer_address, av.country_name as vendor_country,
        #             av.province_name as vendor_province, av.city_name as vendor_city, av.address as vendor_address,
        #             o.order_id, o.status, o.delivery_time, a.content
        #     FROM orders o
        #     LEFT JOIN products p ON o.product_id = p.product_id
        #     LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
        #     LEFT JOIN customers c ON o.customer_id = c.customer_id
        #     LEFT JOIN addresses_customer ac ON o.address_id = ac.address_id
        #     LEFT JOIN addresses_vendor av ON v.vendor_id = av.vendor_id
        #     LEFT JOIN announcements a ON o.order_id = a.order_id
        #     WHERE o.order_id = %s
        # '''

        query = '''
                    SELECT v.vendor_name, v.email as vendor_email, v.phone as vendor_phone, ac.receiver_name as customer_name, c.email as customer_email, 
                           ac.receiver_phone as customer_phone, ac.country_name as customer_country, ac.province_name as customer_province,
                            ac.city_name as customer_city, ac.address as customer_address, av.country_name as vendor_country,
                            av.province_name as vendor_province, av.city_name as vendor_city, av.address as vendor_address, 
                            o.order_id, o.status, o.delivery_time, a.content
                    FROM orders o
                    LEFT JOIN products p ON o.product_id = p.product_id
                    LEFT JOIN vendors v ON p.vendor_id = v.vendor_id
                    LEFT JOIN customers c ON o.customer_id = c.customer_id
                    LEFT JOIN addresses_customer ac ON o.address_id = ac.address_id
                    LEFT JOIN addresses_vendor av ON v.vendor_id = av.vendor_id
                    LEFT JOIN 
                        (SELECT order_id, MAX(announcement_date) as MaxTime
                         FROM announcements
                         GROUP BY order_id) a1 ON o.order_id = a1.order_id
                    LEFT JOIN 
                        announcements a ON a.order_id = a1.order_id AND a.announcement_date = a1.MaxTime
                    WHERE o.order_id = %s
                '''
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()

        if not order:
            return redirect(url_for('vendor_order.order_view'))

        order_detail = dict(zip(cursor.column_names, order))
        if order_detail['delivery_time'] is not None:
            order_detail['delivery_time'] = order_detail['delivery_time'].strftime('%Y-%m-%d')
        print(order_detail)

        query = '''
                   SELECT announcement_date, content 
                   FROM announcements 
                   WHERE order_id = %s 
                   ORDER BY announcement_date DESC
               '''
        cursor.execute(query, (order_id,))
        announcement_rows = cursor.fetchall()

        announcements = []
        for row in announcement_rows:
            announcement_item = {
                'announcement_date': row[0],
                'content': row[1]
            }
            announcements.append(announcement_item)

        cursor.close()
        connection.close()

        return render_template('vendor_order_detail.html', order=order_detail, announcements=announcements)
    else:
        return redirect(url_for('vendor_order.order_view'))


# to update the order status and add announcement
@vendor_order_detail.route('/update_order', methods=['POST'])
def update_order():
    order_id = request.form['order_id']
    order_status = request.form['order_status']
    message = request.form['message']
    delivery_date = request.form['delivery_date']
    print(order_id, order_status, message, delivery_date)

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    query_update_order_status = '''
           UPDATE orders 
           SET status = %s, delivery_time = %s 
           WHERE order_id = %s
       '''
    cursor.execute(query_update_order_status, (order_status, delivery_date, order_id))

    query_insert_announcement = '''
           INSERT INTO announcements (order_id, content) 
           VALUES (%s, %s)
       '''
    cursor.execute(query_insert_announcement, (order_id, message))

    connection.commit()

    return redirect(url_for('vendor_order.order_view'))
