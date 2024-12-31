import random
from Logease.models import Order
from faker import Faker
from datetime import datetime, timedelta
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired
from Logease.models import Order

faker = Faker('id_ID')
    

class orderForm(FlaskForm):
    order_address = StringField('Address', validators=[DataRequired()])
    receiver = StringField('Receiver', validators=[DataRequired()])
    submit = SubmitField('Submit')