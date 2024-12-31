from flask import render_template, Blueprint, request, flash, redirect, url_for
from Logease.main.forms import ResiForm
from Logease.models import Order

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/homepage', methods=['GET', 'POST'])
def home():
    form = ResiForm()
    if form.validate_on_submit():
        resi = form.order_id.data
        order = Order.query.filter_by(order_id=resi).first()
        if order:
            return redirect(url_for('main.resi', order_id=resi))
        else:
            flash('Resi not found!', 'danger')
    return render_template('homepage.html', form=form)

@main.route('/resi/<string:order_id>')
def resi(order_id):
    order = Order.query.filter_by(order_id=order_id).first()
    if order:
        data = order.to_dict()
        return render_template('resi.html', data=data)
    else:
        flash('Resi not found!', 'danger')
        return redirect(url_for('main.home'))