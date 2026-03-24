import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desk_reserve.settings')
django.setup()

from api.models import Workspace

def seed_workspaces():
    # Clear existing data to start fresh (Optional)
    # Workspace.objects.all().delete()

    resource_configs = [
        {'type': 'Desk', 'count': 30, 'capacity': 1},
        {'type': 'Focus Pod', 'count': 10, 'capacity': 1},
        {'type': 'Boardroom', 'count': 2, 'capacity': 10},
    ]

    for floor in range(1, 5): # Floors 1 to 4
        print(f"Seeding Floor {floor}...")
        for config in resource_configs:
            for i in range(1, config['count'] + 1):
                name = f"{config['type']} {floor}.{i:02d}"
                Workspace.objects.get_or_create(
                    name=name,
                    resource_type=config['type'],
                    floor=floor,
                    capacity=config['capacity'],
                    is_active=True
                )

    print("Successfully seeded 168 workspaces!")

if __name__ == "__main__":
    seed_workspaces()