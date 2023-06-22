import os
import random
import time
from datetime import datetime

import mysql.connector
from alipay import AliPay
from db_config import db_connection
from flask import Blueprint, request, redirect, url_for

alipay = Blueprint('alipay', __name__)


# read the content of the file_path
def load_key_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()


# get the absolute path of the file
def get_abs_path(relative_path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


# generate the order id
def generate_out_trade_no():
    timestamp = int(time.time() * 1000)
    random_num = random.randint(1000, 9999)
    return f"{timestamp}{random_num}"


app_private_key_path = get_abs_path('../pay/app_private_key.pem')
alipay_public_key_path = get_abs_path('../pay/alipay_public_key.pem')

app_private_key_string = load_key_from_file(app_private_key_path)
alipay_public_key_string = load_key_from_file(alipay_public_key_path)

# create the alipay client
alipay_client = AliPay(
    appid="2021000122658399",
    app_notify_url=None,
    app_private_key_string=app_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2",
    debug=True
)


# create the payment
@alipay.route('/create_payment', methods=['GET', 'POST'])
def create_payment():
    total_amount = request.form.get('discounted_price')
    order_id = request.form.get('payment_id')
    subject = "product"

    return_url = f"http://127.0.0.1:5000/alipay/alipay_callback?order_id={order_id}"
    order_string = alipay_client.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=total_amount,
        subject=subject,
        return_url=return_url,
        notify_url=None,
    )
    pay_url = f"https://openapi-sandbox.dl.alipaydev.com/gateway.do?{order_string}"
    return redirect(pay_url)


# callback function
@alipay.route('/alipay_callback', methods=['GET', 'POST'])
def alipay_callback():
    data = request.args.to_dict()

    signature = data.pop("sign", None)
    if signature is None:
        return "failed"

    payment_id = data.get("out_trade_no")
    # trade_no = data.get("trade_no")

    connection = mysql.connector.connect(**db_connection)
    cursor = connection.cursor()

    update_orders_query = "UPDATE orders SET status = 'paid' WHERE payment_id = %s"
    cursor.execute(update_orders_query, (payment_id,))
    connection.commit()

    now = datetime.now()
    # Update payments table status to 'paid'
    update_payments_query = "UPDATE payment SET payment_status = 'paid', finish_time = %s  WHERE payment_id = %s"
    cursor.execute(update_payments_query, (now, payment_id,))
    connection.commit()

    # Close the database connection
    cursor.close()
    connection.close()

    return redirect(url_for('order.order_page'))

