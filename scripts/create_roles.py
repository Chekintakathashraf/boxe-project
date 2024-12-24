from users.models import Role

def run():
    roles = ["monitor", "sales", "production", "accounts", "auditor", "dispatch"]

    for role_name in roles:
        role, created = Role.objects.get_or_create(
            role_name=role_name,
            defaults={
               
            }
        )
        if created:
            print(f"Role '{role_name}' created successfully.")
        else:
            print(f"Role '{role_name}' already exists.")