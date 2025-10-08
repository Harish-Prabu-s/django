from django.core.management.base import BaseCommand
from api.models import Bus
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = "Load sample bus data into the database"

    def handle(self, *args, **kwargs):
        bus_names = ["Volvo", "FlixBus", "RedBus", "SuperBus", "ExpressLine", "LuxuryCoach"]
        cities = ["Chennai", "Bangalore", "Hyderabad", "Mumbai", "Pune", "Kolkata", "Delhi", "Coimbatore", "Vizag",
                  "Mysore"]

        for i in range(30):
            source, destination = random.sample(cities, 2)  # Ensure source != destination
            bus_name = random.choice(bus_names)
            bus_number = f"TN{random.randint(1, 99):02d}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{random.randint(1000, 9999)}"
            departure_time = datetime.now() + timedelta(hours=random.randint(1, 12))
            arrival_time = departure_time + timedelta(hours=random.randint(4, 10))
            total_seats = random.choice([40, 45, 50, 55, 60])
            available_seats = total_seats
            fare = random.choice([300, 400, 500, 600, 700])

            bus = Bus.objects.create(
                bus_name=bus_name,
                bus_number=bus_number,
                source=source,
                destination=destination,
                total_seats=total_seats,
                available_seats=available_seats,
                departure_time=departure_time,
                arrival_time=arrival_time,
                fare=fare,
                date=datetime.today().date() + timedelta(days=random.randint(0, 10))
            )
            self.stdout.write(self.style.SUCCESS(f"Bus created: {bus.bus_name} from {source} to {destination}"))

        self.stdout.write(self.style.SUCCESS("30 bus records created successfully!"))
