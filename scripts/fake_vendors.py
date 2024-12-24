from faker import Faker
from vendor.models import Vendor, Sequence
import random

fake = Faker()

def generate_vendors(n=10):
    for _ in range(n):
        vendor_name = fake.company()
        email = fake.unique.email()
        address = fake.address()
        Vendor.objects.create(
            vendor_name=vendor_name,
            email=email,
            address=address
        )

def generate_sequences(vendor, n=3):
    types = ['purchase order', 'sales order', 'payment']
    random.shuffle(types)  # Ensure unique combination of type and vendor
    for i in range(min(n, len(types))):  # Limit to unique types per vendor
        type_choice = types[i]
        alpha = fake.word().upper()[:3]
        numeric = fake.random_int(min=1000, max=9999)
        padding = random.randint(5, 10)
        Sequence.objects.create(
            type=type_choice,
            alpha=alpha,
            numeric=numeric,
            padding=padding,
            vendor=vendor
        )

def run():
    generate_vendors(20)
    vendors = Vendor.objects.all()
    for vendor in vendors:
        generate_sequences(vendor, n=3)
