from flask import Flask, request, redirect, render_template, session, flash, jsonify, url_for, json
import urllib

from sqlalchemy import desc, distinct, create_engine, asc
from flask_sqlalchemy import SQLAlchemy

from flask_sslify import SSLify
from werkzeug.middleware.proxy_fix import ProxyFix
import uuid
import datetime as dt
from flask import Flask
from flask_mail import Mail, Message

server = 'finefolio.database.windows.net'
database = 'ff_1'
username = 'fine_folio'
password = 'Dcapital10!'
driver = '{ODBC Driver 17 for SQL Server}'
# for real azure '{ODBC Driver 17 for SQL Server}'
# for azure from local '{SQL Server}' - you will need to update firewall in order to run this connection

conn = ('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
params = urllib.parse.quote_plus(conn)
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str, echo=True)

#print('connection is ok')
#print(engine_azure.table_names())



app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.secret_key = 'eksewgsdfd@fdsSFDF!234'
app.config['SQLALCHEMY_DATABASE_URI'] = conn_str #'sqlite:///lenses.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config.update(dict(PREFERRED_URL_SCHEME = 'https'))
db = SQLAlchemy(app)
sslify = SSLify(app)
app.wsgi_app = ProxyFix(app.wsgi_app,x_proto=1, x_host=1)
#mail= Mail(app)
app.config['MAIL_SERVER']='smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dzyuba.stanislaw@mail.ru'
app.config['MAIL_PASSWORD'] = 'Dcapital13!'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from models import lenses, lens_images, shopping_cart, orders
from forms import AddToCart, ShoppCartItem, ShoppingCartSubmit, FindOrder

@app.route("/", methods=["POST", "GET"])
def home():
    isshopcart = False
    temp_uid = session.get("temp_uid", None)
    category_displayed_names = {'blue': 'Голубые Линзы', 'gray': 'Серые Линзы', 'green': 'Зеленые Линзы',
                                'brown': 'Карие Линзы', 'black': 'Черные Линзы'}
    if temp_uid == None:
        temp_uid = uuid.uuid4().hex
        session["temp_uid"] = temp_uid
        db_cartitems = None
    else:
        db_cartitems = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
        db.session.close()
    db_displayed_lens = db.session.query(lenses.brand,lenses.color_name,lenses.price).filter().order_by(desc(lenses.stock)).limit(6).all()
    db.session.close()
    displayed_lenses = []
    for each in range(len(db_displayed_lens)):
        db_image_path = db.session.query(lens_images.image_path).filter(
            lens_images.brand == str(db_displayed_lens[each][0]), lens_images.color_name == str(db_displayed_lens[each][1]),
            lens_images.display_order == 1).first()
        item = {"brand": str(db_displayed_lens[each][0]),"color_name": str(db_displayed_lens[each][1]),
                "price": str(round(db_displayed_lens[each][2])), "image_path": str(db_image_path[0])}
        displayed_lenses.append(item)
    items = displayed_lenses

    return render_template("index.html", items = displayed_lenses, isshopcart=isshopcart,
                           db_cartitems = db_cartitems, category_displayed_names=category_displayed_names)

@app.route("/category_<category_name>", methods=["POST", "GET"])
def category(category_name):
    category_displayed_names = {'blue':'Голубые Линзы','gray':'Серые Линзы','green':'Зеленые Линзы',
    'brown':'Карие Линзы','black':'Черные Линзы'}
    category_displayed_name = category_displayed_names[category_name]
    isshopcart = False
    temp_uid = session.get("temp_uid", None)
    if temp_uid == None:
        temp_uid = uuid.uuid4().hex
        session["temp_uid"] = temp_uid
        db_cartitems = None
    else:
        db_cartitems = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
        db.session.close()
    db_displayed_lens = db.session.query(lenses.brand,lenses.color_name,lenses.price).filter(lenses.color_category == category_name).distinct().all()
    db.session.close()
    displayed_lenses = []
    for each in range(len(db_displayed_lens)):
        db_image_path = db.session.query(lens_images.image_path).filter(
            lens_images.brand == str(db_displayed_lens[each][0]), lens_images.color_name == str(db_displayed_lens[each][1]),
            lens_images.display_order == 1).first()
        item = {"brand": str(db_displayed_lens[each][0]),"color_name": str(db_displayed_lens[each][1]),
                "price": str(round(db_displayed_lens[each][2])), "image_path": str(db_image_path[0])}
        displayed_lenses.append(item)
    items = displayed_lenses

    return render_template("category.html", items = displayed_lenses, isshopcart=isshopcart,
                           category_displayed_name=category_displayed_name,
                           category_displayed_names = category_displayed_names, db_cartitems=db_cartitems)



@app.route("/item_<item_name>", methods=["POST", "GET"])
def item(item_name):
    isshopcart = False
    temp_uid = session.get("temp_uid", None)
    if temp_uid == None:
        temp_uid = uuid.uuid4().hex
        session["temp_uid"] = temp_uid
        db_cartitems = None
    else:
        db_cartitems = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
        db.session.close()
    category_displayed_names = {'blue': 'Голубые Линзы', 'gray': 'Серые Линзы', 'green': 'Зеленые Линзы',
                                    'brown': 'Карие Линзы', 'black': 'Черные Линзы'}
    image_path = 'http://placehold.it/900x400'
    item = item_name.split("+")
    brand = item[0]
    color_name = item[1]
    replacement_frequency = db.session.query(lenses.replacement_frequency).filter(lenses.brand == brand, lenses.color_name == color_name).first()
    replacement_frequency = replacement_frequency[0]
    if replacement_frequency == 'quarterly':
        replacement_frequency = '3 месяца'
    elif replacement_frequency == 'annual':
        replacement_frequency = '1 год'
    else:
        replacement_frequency = 'something went wrong'
    price_dio = []
    db_price_dio = db.session.query(lenses.price,lenses.dioptrics).filter(lenses.brand == brand,
                                                                          lenses.color_name == color_name).order_by(desc(lenses.dioptrics)).all()
    for i in range(len(db_price_dio)):
        pair = {"price": str(round(db_price_dio[i][0])), "dioptrics": str(db_price_dio[i][1])}
        price_dio.append(pair)
    db_dio = db.session.query(lenses.dioptrics).filter(lenses.brand == brand,
                                                                           lenses.color_name == color_name).order_by(desc(lenses.dioptrics)).all()
    dio = []
    for i in range(len(db_dio)):
        dio.append(db_dio[i][0])
    init_price = price_dio[0]['price']
    db_image_path = db.session.query(lens_images.image_path, lens_images.display_order).filter(lens_images.brand == brand,
                                                                                   lens_images.color_name == color_name).order_by(asc(lens_images.display_order)).all()
    image_paths = []
    for i in range(len(db_image_path)):
        pair = {'display_order': str(db_image_path[i][1]), 'image_path': str(db_image_path[i][0])}
        image_paths.append(pair)

    form = AddToCart()
    form.dioptrics.choices = dio
    form.count.data = 1
    if form.validate_on_submit():
        dioprics_from_ui = form.dioptrics.data
        count_from_ui = int(form.count._value())
        new_shoppcart_item = shopping_cart(temp_uuid=temp_uid,brand = brand, color_name=color_name,
                                           dioptrics=dioprics_from_ui,amount=count_from_ui,timestamp = dt.datetime.today())
        db.session.add(new_shoppcart_item)
        db.session.commit()
        db.session.close()
        print(dioprics_from_ui, count_from_ui, brand, color_name)
        return redirect("/")
    else:
        return render_template("item.html", brand = brand, color_name = color_name, price_dio = price_dio,
                           init_price = init_price, replacement_frequency=replacement_frequency,
                            image_paths = image_paths,form = form, isshopcart=isshopcart,
                               category_displayed_names=category_displayed_names,
                               db_cartitems=db_cartitems)

@app.route("/shopping_cart_page", methods=["POST", "GET"])
def shopping_cart_page():
    isshopcart = True
    temp_uid = session.get("temp_uid", None)
    form = ShoppingCartSubmit()
    db_cartitems = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
    db.session.close()
    cartitems = []
    total = 0
    if db_cartitems:
        form.cart_items.max_entries = len(db_cartitems)
        for i in range(len(db_cartitems)):
            price = db.session.query(lenses.price).filter(lenses.brand == str(db_cartitems[i].brand),
                                                          lenses.color_name == str(db_cartitems[i].color_name),
                                                          lenses.dioptrics == str(db_cartitems[i].dioptrics)).first()
            image_path = db.session.query(lens_images.image_path).filter(lens_images.brand == str(db_cartitems[i].brand),
                                                                         lens_images.color_name == str(db_cartitems[i].color_name),
            lens_images.display_order == 1).first()
            cartitem = {'brand': str(db_cartitems[i].brand), 'color_name': str(db_cartitems[i].color_name),
                        'dioptrics': str(db_cartitems[i].dioptrics), 'amount': int(db_cartitems[i].amount),
                        'price': round(int(price[0])), 'image_path':str(image_path[0])}
            cartitems.append(cartitem)
        for i in cartitems:
            subtotal = i['amount'] * i['price']
            total = total + subtotal
    if form.validate_on_submit():
        name_of_user = form.name_of_user.data
        email = form.email.data
        address = form.address.data
        promo = form.promocode.data
        phone = form.phone.data
        seq_no = db.session.query(orders.seq_no).filter(orders.temp_uuid == temp_uid).order_by(desc(orders.seq_no)).first()
        if seq_no:
            seq_no = int(seq_no[0])+1
        else:
            seq_no = 1
        for i in form.cart_items:
            dio = float(i['dioptrics'].data)
            price = float(i['price'].data)
            brand = i['brand'].data
            color_name = i['color_name'].data
            amount = int(i['amount'].data)
            new_order = orders(temp_uuid=temp_uid, seq_no=seq_no,name=name_of_user, email=email, price=price,
                               brand=brand, color_name=color_name, dioptrics=dio, amount=amount,
                               timestamp=dt.datetime.today(), phone=phone,
                               address=address, promo=promo, status='P', user_id='')
            db.session.add(new_order)
            db.session.commit()
            empty_shopcart = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
            for each in empty_shopcart:
                db.session.delete(each)
                db.session.commit()
                db.session.close()
        msg = Message('lupa: новый заказ с сайта', sender='dzyuba.stanislaw@mail.ru', recipients=['k.tsenilova@mail.ru'])
        msg.body = "#:{}".format(str(seq_no)+'-'+temp_uid)+"; "+ "email: {}".format(email)+" ;address: {}".format(address)\
                   + " ;phone: {}".format(phone)+" ;promo: {}".format(promo)+ " ;cartitems: {}".format(cartitems)
        mail.send(msg)
        flash('Ваш заказ создан, пожалуйста, запишите номер заказа ниже, мы свяжемся с вами в ближайшее время', 'info')
        return redirect("/my_orders")
    return render_template("shopping_cart_page.html", isshopcart=isshopcart, cartitems=cartitems, form=form, total=total, db_cartitems = db_cartitems)

@app.route("/my_orders", methods=["POST", "GET"])
def my_orders():
    isshopcart = True
    temp_uid = session.get("temp_uid", None)
    db_orders_seq_no = db.session.query(distinct(orders.seq_no)).filter(orders.temp_uuid == temp_uid).order_by(desc(orders.seq_no)).all()
    db.session.close()
    displayed_orders = []
    status = None
    form = FindOrder()
    if db_orders_seq_no:
        db_cartitems = db.session.query(shopping_cart).filter(shopping_cart.temp_uuid == temp_uid).all()
        db.session.close()
    else:
        db_cartitems = None
    for i in db_orders_seq_no:
        order_seq_no = i[0]
        order_uid = db.session.query(orders.temp_uuid).filter(orders.temp_uuid == temp_uid, orders.seq_no == order_seq_no).first()
        db_status = db.session.query(orders.status).filter(orders.temp_uuid == temp_uid,orders.seq_no == order_seq_no).first()
        db.session.close()
        if db_status[0] == 'P':
            status = 'В обработке'
        elif db_status[0] == 'D':
            status = 'Отменен'
        elif db_status[0] == 'C':
            status = 'Выдан'
        displayed_order_number = str(order_seq_no) +"-"+ order_uid[0]
        ordered_units=[]
        db_units = db.session.query(orders.brand, orders.color_name, orders.dioptrics, orders.amount,
                                   orders.price).filter(orders.temp_uuid == temp_uid, orders.seq_no == order_seq_no).all()
        db.session.close()
        for i in db_units:
            unit = {'unit_name': i.brand+" "+i.color_name, 'dio': i.dioptrics, 'amount': i.amount, 'price': round(i.price)}
            ordered_units.append(unit)
        orderitem = {'displayed_order_number': displayed_order_number,'status': status, 'ordered_units': ordered_units}
        displayed_orders.append(orderitem)
    if form.validate_on_submit():
        order_id = form.order_id.data.split(sep="-")
        try:
            to_find = order_id[1]
        except:
            to_find = order_id[0]
        session["temp_uid"] = to_find
        return redirect("/my_orders")
    return render_template("my_orders.html", orders=orders, isshopcart=isshopcart, displayed_orders = displayed_orders, form=form,
                           db_cartitems=db_cartitems)