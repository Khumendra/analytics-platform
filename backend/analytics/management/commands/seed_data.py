from django.core.management.base import BaseCommand
from analytics.models import Organization, User, Event
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Seeds database with production-grade isolated baseline structures'

    def handle(self, *args, **kwargs):
        # Clean state setups
        Event.objects.all().delete()
        User.objects.all().delete()
        Organization.objects.all().delete()

        # Create Baseline Tenant
        org = Organization.objects.create(name="Acme Corp Analytics")
        
        # Create High-Tier Administrative Member Nodes
        admin_user = User.objects.create_user(
            username="admin", 
            email="admin@acme.com", 
            password="securepassword123",
            organization=org,
            role="ADMIN"
        )

        # Seed realistic Time-Series Data arrays
        event_actions = ["user_signup", "page_view", "payment_success", "api_call_failed"]
        events_pool = []

        for i in range(150):
            days_offset = random.randint(0, 5)
            mock_time = timezone.now() - timezone.timedelta(days=days_offset)
            events_pool.append(
                Event(
                    organization=org,
                    event_name=random.choice(event_actions),
                    properties={"browser": random.choice(["Chrome", "Safari", "Firefox"]), "latency_ms": random.randint(10, 250)},
                    timestamp=mock_time
                )
            )

        Event.objects.bulk_create(events_pool)
        self.stdout.write(self.style.SUCCESS('Successfully seeded database cluster nodes cleanly!'))