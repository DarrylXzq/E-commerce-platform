import mysql.connector
from db_config import db_connection
from flask import Blueprint, render_template, request, session, redirect, url_for

order_detail = Blueprint('order_detail', __name__)


# display order detail, address, vendor info, and announcements
@order_detail.route('/order_detail_page', methods=['GET', 'POST'])
def order_detail_page():
    if session.get('user_type') == 'customer':
        customer_id = session.get('user_id')
    else:
        return redirect(url_for('login.login_page'))
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        connection = mysql.connector.connect(**db_connection)
        cursor = connection.cursor()

        query = '''
            SELECT v.vendor_name, v.email as vendor_email, v.phone as vendor_phone, ac.receiver_name as customer_name, c.email as customer_email, 
                   ac.receiver_phone as customer_phone, ac.country_name as customer_country, ac.province_name as customer_province,
                    ac.city_name as customer_city, ac.address as customer_address, av.country_name as vendor_country,
                    av.province_name as vendor_province, av.city_name as vendor_city, av.address as vendor_address
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
            return redirect(url_for('order.order_page'))

        order_detail = dict(zip(cursor.column_names, order))

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

        return render_template('order_detail.html', order=order_detail, announcements=announcements)
    else:
        return redirect(url_for('order.order_page'))
