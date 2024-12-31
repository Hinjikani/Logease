from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from Logease.models import Order

class ResiForm(FlaskForm):
    order_id = StringField('Resi', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_resi(self, order_id):
        order = Order.query.filter_by(order_id=order_id.data).first()
        if not order:
            raise ValidationError('Resi not found.')