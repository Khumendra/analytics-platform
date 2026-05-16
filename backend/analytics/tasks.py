from celery import shared_task
from analytics.models import Event, Organization
from django.utils.dateparse import parse_datetime

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def process_bulk_events(self, org_id, events_data):
    """
    Asynchronously clean, normalize, and batch insert events into database.
    """
    try:
        org = Organization.objects.get(id=org_id)
        events_to_create = []
        
        for item in events_data:
            events_to_create.append(
                Event(
                    organization=org,
                    event_name=item['event_name'],
                    properties=item.get('properties', {}),
                    timestamp=parse_datetime(item['timestamp'])
                )
            )
        
        # Batch upload to leverage bulk insert speeds
        Event.objects.bulk_create(events_to_create)
        return f"Successfully processed {len(events_to_create)} metrics for Org: {org_id}"
    except Exception as exc:
        raise self.retry(exc=exc)