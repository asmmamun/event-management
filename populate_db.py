import os
import django
import random
from faker import Faker
from events.models import Event, Participant, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

def populate_db():
    fake = Faker()

    # Create Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.sentence()
    ) for _ in range(3)]
    print(f"Created {len(categories)} categories.")

    # Create Events
    events = [Event.objects.create(
        name=fake.sentence(nb_words=4),
        description=fake.paragraph(),
        date=fake.date_this_year(),
        time=fake.time(),
        location=fake.city(),
        category=random.choice(categories)
    ) for _ in range(5)]
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = [Participant.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]
    print(f"Created {len(participants)} participants.")

    # Assign Participants to Events
    for event in events:
        selected_participants = random.sample(participants, random.randint(1, 5))
        event.participants.set(selected_participants)

    print("Database populated successfully!")

# Run the function
if __name__ == "__main__":
    populate_db()
