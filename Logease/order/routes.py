from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask_login import current_user
from Logease import db
from Logease.models import Order, Armada
from Logease.order.forms import orderForm
from faker import Faker
from datetime import datetime, timedelta
import random

order = Blueprint('order', __name__)
faker = Faker("id_ID")

@order.route('/order_dash', methods=['GET', 'POST'])
def order_dash():
    form = orderForm()
    if form.validate_on_submit():
        armadas = Armada.query.all()
        new_order = Order(
            user_id=current_user.id,
            armada_id=random.choice(armadas).id,
            order_id=faker.uuid4(),
            address=form.order_address.data,
            order_date=datetime.now(),
            arrival_estimation=datetime.now() + timedelta(days=random.randint(1, 10)),
            status='Pending',
            current_location=form.order_address.data,
            receiver=form.receiver.data,
            order_fee=round(random.uniform(5000.0, 50000.0), 2)
        )
        db.session.add(new_order)
        db.session.commit()
        flash("Order has been created!", 'success')
        return redirect(url_for('order.order_dash'))
    return render_template('order_dashboard.html', form=form)
