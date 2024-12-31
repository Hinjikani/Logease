import random
import sys
from faker import Faker
from datetime import datetime, timedelta
from Logease import create_app, db
from Logease.models import Order, User, Armada

app = create_app()
app.app_context().push()

faker = Faker("id_ID")

def create_fake_orders(n):
    """Generate fake orders."""
    users = User.query.all()
    armadas = Armada.query.all()
    
    if not users or not armadas:
        print("Ensure there are users and armadas in the database before creating orders.")
        return

    for _ in range(n):
        user = random.choice(users)
        armada = random.choice(armadas)
        order = Order(
            order_id=faker.uuid4(),
            address=faker.address().replace('\n', ', '),
            order_date=faker.date_time_this_year(),
            arrival_estimation=faker.date_time_this_year() + timedelta(days=random.randint(1, 10)),
            status=random.choice(['Pending', 'Ready', 'On Shipping', 'Delivered', 'Cancelled']),
            current_location=faker.city(),
            receiver=faker.name(),
            order_fee=round(random.uniform(5000.0, 50000.0), 2),
            armada_id=armada.id,
            user_id=user.id
        )
        db.session.add(order)
    db.session.commit()
    print(f'Added {n} fake orders to the database.')

def create_fake_armadas(n):
    """Generate fake armadas."""
    for _ in range(n):
        armada = Armada(
            armada_name=faker.company(),
            armada_id=faker.uuid4(),
            armada_phone=faker.phone_number(),
            armada_email=faker.company_email(),
            armada_status=random.choice(['Active', 'Inactive']),
            capacity=round(random.uniform(0.0, 100.0), 2)
        )
        db.session.add(armada)
    db.session.commit()
    print(f'Added {n} fake armadas to the database.')

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Pass the number of armadas and orders you want to create as arguments.')
        sys.exit(1)
    create_fake_armadas(int(sys.argv[1]))
    create_fake_orders(int(sys.argv[2]))
