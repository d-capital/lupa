from app import db

class lenses(db.Model):
    brand = db.Column(db.String(100), primary_key=True)
    color_name = db.Column(db.String(1000), primary_key=True)
    dioptrics = db.Column(db.Float, primary_key=True)
    replacement_frequency = db.Column(db.String(100), primary_key=True)
    color_category = db.Column(db.String(100))
    unit = db.Column(db.Integer)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)

    def __init__(self, brand, color_name, dioptrics, replacement_frequency, color_category, unit, price, stock):
        self.brand = brand
        self.color_name = color_name
        self.dioptrics = dioptrics
        self.replacement_frequency = replacement_frequency
        self.color_category = color_category
        self.unit = unit
        self.price = price
        self.stock = stock

class lens_images(db.Model):
    brand = db.Column(db.String(100), primary_key=True)
    color_name = db.Column(db.String(1000), primary_key=True)
    display_order = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(1000))

    def __init__(self, brand, color_name, display_order, image_path):
        self.brand = brand
        self.color_name = color_name
        self.display_order = display_order
        self.image_path = image_path

class shopping_cart(db.Model):
    temp_uuid = db.Column(db.String(1000), primary_key=True)
    brand = db.Column(db.String(100))
    color_name = db.Column(db.String(1000))
    dioptrics = db.Column(db.Float)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, primary_key = True)

    def __init__(self, temp_uuid, brand, color_name, dioptrics, amount, timestamp):
        self.temp_uuid = temp_uuid
        self.brand = brand
        self.color_name = color_name
        self.dioptrics = dioptrics
        self.amount = amount
        self.timestamp = timestamp

class orders(db.Model):
    temp_uuid = db.Column(db.String(1000), primary_key=True)
    seq_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(300))
    price = db.Column(db.Float)
    brand = db.Column(db.String(100), primary_key=True)
    color_name = db.Column(db.String(1000), primary_key=True)
    dioptrics = db.Column(db.Float, primary_key=True)
    amount = db.Column(db.Integer,primary_key=True)
    timestamp = db.Column(db.DateTime, primary_key=True)
    phone = db.Column(db.String(500))
    address = db.Column(db.String(500))
    promo = db.Column(db.String(500))
    status = db.Column(db.String(20))
    user_id = db.Column(db.Integer)

    def __init__(self, temp_uuid, seq_no, name, email, price, brand, color_name, dioptrics, amount, timestamp, phone, address, promo, status, user_id):
        self.temp_uuid = temp_uuid
        self.seq_no = seq_no
        self.name = name
        self.email = email
        self.price = price
        self.brand = brand
        self.color_name = color_name
        self.dioptrics = dioptrics
        self.amount = amount
        self.timestamp = timestamp
        self.phone = phone
        self.address = address
        self.promo = promo
        self.status = status
        self.user_id = user_id