from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from Logease import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    privilege = db.Column(db.Enum('admin', 'user', 'armada'), nullable=False,  default='user')
    order = db.relationship('Order', backref='sender', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age=max_age)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'privilege': self.privilege
        }

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc))
    arrival_estimation = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('Pending', 'Ready', 'On Shipping', 'Delivered', 'Cancelled'), default='Pending', nullable=False)
    current_location = db.Column(db.String(100), nullable=False)
    receiver = db.Column(db.String(100), nullable=False)
    order_fee = db.Column(db.Float)
    armada_id = db.Column(db.Integer, db.ForeignKey('armada.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'address': self.address,
            'order_date': self.order_date,
            'current_location': self.current_location,
            'arrival_estimation': self.arrival_estimation,
            'status': self.status,
            'receiver': self.receiver,
            'order_fee': self.order_fee,
            'armada_id': self.armada_id,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f"Order('{self.order_id}', '{self.order_date}, '{self.order_status}', '{self.reciever}', '{self.driver_id}', '{self.user_id}')"

class Armada(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    armada_name = db.Column(db.String(100), nullable=False)
    armada_id = db.Column(db.String(100), nullable=False)
    armada_phone = db.Column(db.String(100), nullable=False)
    armada_email = db.Column(db.String(100), nullable=False)
    armada_status = db.Column(db.Enum('Active', 'Inactive'), nullable=False)
    capacity = db.Column(db.Float, nullable=False)
    order = db.relationship('Order', backref='driver', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'armada_name': self.armada_name,
            'armada_id': self.armada_id,
            'armada_phone': self.armada_phone,
            'armada_email': self.armada_email,
            'armada_status': self.armada_status,
            'capacity': self.capacity
        }

    def __repr__(self):
        return f"Drivers('{self.driver_name}', '{self.driver_id}', '{self.driver_phone}', '{self.driver_email}', '{self.driver_status}')"