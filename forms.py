from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,Form,IntegerField,SelectField,BooleanField,DateField,\
    FormField,FieldList, FloatField
from wtforms.validators import DataRequired,length, NumberRange, Email, Length
from wtforms.fields.html5 import EmailField, TelField
from wtforms import validators

class AddToCart(FlaskForm):
    dioptrics = SelectField('dioptric', validators=[DataRequired()])
    count = IntegerField('count',validators=[DataRequired(),NumberRange(min=1, max=10)])
    submit = SubmitField('submit')

class ShoppCartItem(Form):
    brand = StringField('brand')
    color_name = StringField('color_name')
    dioptrics = FloatField('dioptrics')
    amount = IntegerField('amount', validators=[DataRequired(), NumberRange(min=1, max=10)])
    price = FloatField('price')

class ShoppingCartSubmit(FlaskForm):
    name_of_user = StringField('name_of_user', [validators.DataRequired(), validators.Length(max=400)])
    email = EmailField('email', [validators.DataRequired(), validators.Email()])
    phone = TelField('telfield', [validators.DataRequired()])
    promocode = StringField('promocode')
    cart_items = FieldList(FormField(ShoppCartItem), min_entries=1, max_entries=30)
    address = StringField('address', [validators.DataRequired(), validators.Length(max=400)])
    pi_data = BooleanField('pi_data', validators=[DataRequired()])
    submit = SubmitField('submit')

class FindOrder(FlaskForm):
    order_id = StringField('order_id', [validators.DataRequired(), validators.Length(max=400)])
    submit = SubmitField('submit')