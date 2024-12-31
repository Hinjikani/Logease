from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, SelectField
from wtforms.validators import DataRequired
from Logease.models import Order

class statusForm(FlaskForm):
    order_id = StringField('Resi', validators=[DataRequired()])
    current_location = StringField('Current Location', validators=[DataRequired()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Ready', 'Ready'), ('On Shipping', 'On Shipping'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_resi(self, order_id):
        order = Order.query.filter_by(order_id=order_id.data).first()
        if not order:
            raise ValidationError('Resi not found.')