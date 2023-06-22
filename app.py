import random

from captcha.image import ImageCaptcha
from customer.cart import cart
from customer.checkout import checkout
from customer.comment import comment
from customer.detail import detail
from customer.home import home
from customer.login import login
from customer.nav_user import nav_user
from customer.order import order
from customer.register import register
from customer.order_detail import order_detail

from flask import Flask, make_response, redirect, url_for

from pay.alipay import alipay

from vendor.vendor_info import vendor_info
from vendor.vendor_order import vendor_order
from vendor.vendor_upload import vendor_upload
from vendor.vendor_view import vendor_view
from vendor.vendor_order_detail import vendor_order_detail

app = Flask(__name__)
app.secret_key = 'Darryl_Xiang'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_PRODUCT'] = '../static/products'

image_captcha = ImageCaptcha()

app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(register, url_prefix='/register')
app.register_blueprint(nav_user, url_prefix='/nav_user')
app.register_blueprint(home, url_prefix='/home')
app.register_blueprint(detail, url_prefix='/detail')
app.register_blueprint(comment, url_prefix='/comment')
app.register_blueprint(cart, url_prefix='/cart')
app.register_blueprint(checkout, url_prefix='/checkout')
app.register_blueprint(order, url_prefix='/order')
app.register_blueprint(order_detail, url_prefix='/order_detail')

app.register_blueprint(vendor_upload, url_prefix='/vendor_upload')
app.register_blueprint(vendor_view, url_prefix='/vendor_view')
app.register_blueprint(vendor_info, url_prefix='/vendor_info')
app.register_blueprint(vendor_order, url_prefix='/vendor_order')
app.register_blueprint(vendor_order_detail, url_prefix='/vendor_order_detail')

app.register_blueprint(alipay, url_prefix='/alipay')


@app.route('/captcha_image', methods=['GET'])
def captcha_image():
    captcha_text = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ123456789', k=4))
    image_data = image_captcha.generate(captcha_text)

    response = make_response(image_data.read())
    response.headers.set('Content-Type', 'image/png')
    response.set_cookie('captcha', captcha_text, max_age=60)
    return response


@app.route('/')
def index():
    return redirect(url_for('home.home_page'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True)
