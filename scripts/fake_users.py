from users.models import User, Role
from faker import Faker
import random
import re

def run():
    fake = Faker()

    roles = Role.objects.all()

    if not roles:
        print("No roles found in the database. Please ensure roles are created first.")
        return

    for _ in range(30): 
        role = random.choice(roles)

        fake_name = fake.name()
        fake_email = fake.email()
        fake_phone_number = re.sub(r'\D', '', fake.unique.phone_number())[:10]  # Generates 10-digit phone number
        password = fake.password()

        user = User.objects.create(
            email=fake_email,
            phone_number=fake_phone_number,
            password=password,
            role=role,
            name=fake_name,
        )

        print(f"User {user.email} with phone number {user.phone_number} created for role {role.role_name}.")


