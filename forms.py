from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,Form,IntegerField,SelectField,BooleanField,DateField,\
    FormField,FieldList, FloatField
from wtforms.validators import DataRequired,length, NumberRange, Email, Length, ValidationError
from wtforms.fields import EmailField, TelField
from wtforms import validators
import phonenumbers
import email_validator

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
    name_of_user = StringField('name_of_user', [validators.DataRequired(),
                                                validators.Length(max=300, message="Попробуйте ввести более короткое имя")])
    email = EmailField('email', [validators.DataRequired(), validators.Email("Пожалуйста, введите свой e-mail корректно.")])
    phone = TelField('telfield', [validators.DataRequired()])
    promocode = StringField('promocode')
    cart_items = FieldList(FormField(ShoppCartItem), min_entries=1, max_entries=30)
    address = StringField('address', [validators.DataRequired(), validators.Length(max=200, message="Вы ввели слишком длинный адрес.")])
    pi_data = BooleanField('pi_data', validators=[DataRequired()])
    submit = SubmitField('submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Некорректно введен номер телефона. Введите его в формате +7XXXXXXXXXX')

class FindOrder(FlaskForm):
    order_id = StringField('order_id', [validators.DataRequired(), validators.Length(max=400)])
    submit = SubmitField('submit')