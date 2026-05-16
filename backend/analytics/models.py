import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Organization(models.Model):
    """
    SaaS Tenant Model. Every organization has isolated data layers.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    Custom User Model supporting explicit Role Hierarchies.
    """
    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Owner'
        ADMIN = 'ADMIN', 'Admin'
        ANALYST = 'ANALYST', 'Analyst'
        VIEWER = 'VIEWER', 'Viewer'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)

    # Resolve reverse accessor clashes with default auth.User
    groups = models.ManyToManyField('auth.Group', related_name='analytics_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='analytics_user_set', blank=True)

class Event(models.Model):
    """
    Highly optimized multi-tenant, time-series telemetry event model.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='events')
    event_name = models.CharField(max_length=255, db_index=True)
    
    # Store dynamic event payloads using Postgres JSONB
    properties = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Senior Architecture Indexing strategy for fast aggregations
        indexes = [
            models.Index(fields=['organization', 'timestamp', 'event_name']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.organization.name} - {self.event_name}"