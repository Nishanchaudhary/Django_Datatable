# datatables_app/management/commands/populate_sample_data.py

from django.core.management.base import BaseCommand
from datatables_app.models import Customer, Product
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Clear existing data
        Customer.objects.all().delete()
        Product.objects.all().delete()
        
        self.stdout.write('Creating sample customers...')
        # Create sample customers
        customers = []
        for i in range(50):
            customer = Customer(
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number()[:15],
                address=fake.address().replace('\n', ', ')[:100],
                city=fake.city(),
                country=fake.country(),
                created_at=fake.date_time_this_year()
            )
            customers.append(customer)
        
        Customer.objects.bulk_create(customers)
        
        self.stdout.write('Creating sample products...')
        # Create sample products
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Toys', 'Beauty']
        products = []
        for i in range(30):
            product = Product(
                name=fake.word().title() + ' ' + fake.word().title(),
                category=random.choice(categories),
                price=round(random.uniform(10, 1000), 2),
                quantity=random.randint(0, 100),
                description=fake.text(max_nb_chars=200),
                is_available=random.choice([True, False]),
                created_at=fake.date_time_this_year()
            )
            products.append(product)
        
        Product.objects.bulk_create(products)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {Customer.objects.count()} customers and {Product.objects.count()} products'
            )
        )