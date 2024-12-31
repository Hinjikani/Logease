from flask import render_template, Blueprint, request, flash, redirect, url_for
from Logease import db
from Logease.models import Order
from Logease.armada.forms import statusForm

armada = Blueprint('armada', __name__)

@armada.route('/armada_dashboard', methods=['GET', 'POST'])
def armada_dash():
    form = statusForm()
    if form.validate_on_submit():
        order = Order.query.filter_by(order_id=form.order_id.data).first()
        if order:
            order.current_location = form.current_location.data
            order.status = form.status.data
            db.session.commit()
            flash('Order status has been updated!', 'success')
        else:
            flash('Order not found!', 'danger')
        return redirect(url_for('armada.armada_dash'))
    return render_template('armada_dashboard.html', form=form)