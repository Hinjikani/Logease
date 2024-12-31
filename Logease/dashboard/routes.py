from flask import render_template, Blueprint, request, abort, flash, redirect, url_for
from flask_login import current_user
from Logease import db
from Logease.models import Order, Armada, User
from Logease.dashboard.forms import ArmadaForm, UserPrivilege
from sqlalchemy import func
from faker import Faker


dash = Blueprint('dash', __name__)
faker = Faker("id_ID")

@dash.route('/')
@dash.route('/dashboard')
def dashboard():
    orders_count = Order.query.count()
    pending_orders_count = Order.query.filter_by(status='Pending').count()
    on_progress_count = Order.query.filter_by(status='On Shipping').count()
    delivered_count = Order.query.filter_by(status='Delivered').count()
    return render_template('dashboard.html', orders_count=orders_count, ready_count=pending_orders_count, on_progress_count=on_progress_count, delivered_count=delivered_count, dashboard = True)

@dash.route('/dashboard/armada')
def armada_dashboard():
    armada_count = Armada.query.count()
    active_armada_count = Armada.query.filter_by(armada_status='Active').count()
    inactive_armada_count = Armada.query.filter_by(armada_status='Inactive').count()
    average_capacity = db.session.query(func.avg(Armada.capacity)).scalar()
    if average_capacity != None:
        average_capacity = round(average_capacity, 2)
    return render_template('armada.html', armada_count=armada_count, active_armada_count=active_armada_count, inactive_armada_count=inactive_armada_count, armada = True, average_capacity=average_capacity)

@dash.route('/dashboard/admin')
def admin_dashboard():
    return render_template('admin.html', admin = True)

@dash.route('/api/data/order')
def order_data():
    query = Order.query

    #search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Order.order_id.like(f'%{search}%'),
            Order.receiver.like(f'%{search}%'),
            Order.address.like(f'%{search}%'),
        ))
    total = query.count()

    #pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    #response
    return {
        'data': [order.to_dict() for order in query.all()],
        'total': total,
    }

@dash.route('/api/data/user')
def user_data():
    query = User.query

    #search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            User.username.like(f'%{search}%'),
        ))
    total = query.count()

    #pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    #response
    return {
        'data': [user.to_dict() for user in query.all()],
        'total': total,
    }

@dash.route('/api/data/user', methods=['POST'])
def user_update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    user = User.query.get(data['id'])
    for field in ['username', 'email', 'privilege']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return '', 204

@dash.route('/dashboard/user_privilege', methods=['GET', 'POST'])
def privilege():
    form = UserPrivilege()
    if form.validate_on_submit():
        user = User.query.get(form.user_id.data)
        if user:
            user.privilege = form.privilege.data
            db.session.commit()
            flash('User privilege has been updated!', 'success')
        else:
            flash('User not found!', 'danger')
        return redirect(url_for('dash.dashboard'))
    return render_template('user_privilege.html', title='User Privilege', form=form)

@dash.route('/dashboard/register_armada', methods=['GET', 'POST'])
def register_armada():
    form = ArmadaForm()
    if form.validate_on_submit():
        armada = Armada(
            armada_name=form.armada_name.data,
            armada_phone=form.armada_phone.data,
            armada_email=form.armada_email.data,
            armada_status='Active',
            capacity= 0.0,
            armada_id= faker.uuid4()
        )
        db.session.add(armada)
        db.session.commit()
        flash('Armada has been registered!', 'success')
        return redirect(url_for('dash.dashboard'))
    return render_template('register_armada.html', form=form)

@dash.route('/api/data/order', methods=['POST'])
def order_update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    order = Order.query.get(data['id'])
    for field in ['order_id', 'order_data', 'arrival_estimation', 'receiver', 'current_location', 'order_fee', 'armada_id', 'user_id']:
        if field in data:
            setattr(order, field, data[field])
    db.session.commit()
    return '', 204

@dash.route('/api/data/armada')
def armada():
    query = Armada.query

    #search filter
    search = request.args.get('search')
    if search:
        query = query.filter(db.or_(
            Armada.armada_name.like(f'%{search}%'),
            Armada.email.like(f'%{search}%'),
            Armada.armada_id.like(f'%{search}%'),
        ))
    total = query.count()

    #pagination
    start = request.args.get('start', type=int, default=-1)
    length = request.args.get('length', type=int, default=-1)
    if start != -1 and length != -1:
        query = query.offset(start).limit(length)

    #response
    return {
        'data': [armada.to_dict() for armada in query.all()],
        'total': total,
    }

@dash.route('/api/data/armada', methods=['POST'])
def armada_update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    armada = Armada.query.get(data['id'])
    for field in ['armada_name', 'armada_id', 'armada_phone', 'armada_email', 'armada_status', 'capacity']:
        if field in data:
            setattr(armada, field, data[field])
    db.session.commit()
    return '', 204