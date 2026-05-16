from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay

from analytics.models import Event
from analytics.serializers import EventSerializer, CustomTokenObtainPairSerializer
from analytics.permissions import IsAnalystOrAbove, IsViewerOrAbove
from analytics.tasks import process_bulk_events
from rest_framework_simplejwt.views import TokenObtainPairView

# Custom Token Overwrite
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Pydantic Structural Contract schemas
class SingleEventSchema(BaseModel):
    event_name: str = Field(..., min_length=1)
    properties: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: timezone.now().isoformat())

class BatchIngestSchema(BaseModel):
    events: List[SingleEventSchema]

class DataIngestionView(APIView):
    """
    Asynchronous ingestion API boundary protecting multi-tenant nodes.
    """
    permission_classes = [IsAuthenticated, IsAnalystOrAbove]

    def post(self, request):
        try:
            # Perform runtime performance validation via Pydantic v2
            payload = BatchIngestSchema(**request.data)
        except ValidationError as e:
            return Response({"errors": e.errors()}, status=status.HTTP_400_BAD_REQUEST)

        # Hand off compute payloads immediately into Redis/Celery cluster Workers
        serialized_events = [event.model_dump() for event in payload.events]
        process_bulk_events.delay(str(request.user.organization.id), serialized_events)

        return Response(
            {"status": "accepted", "message": "Batch enqueued successfully"}, 
            status=status.HTTP_202_ACCEPTED
        )

class DashboardMetricsView(APIView):
    """
    Aggregates analytical database layers optimized by multi-tenant indexing bounds.
    """
    permission_classes = [IsAuthenticated, IsViewerOrAbove]

    def get(self, request):
        org = request.user.organization
        # Multi-tenant context filter enforcement at database query layer
        queryset = Event.objects.filter(organization=org)

        # Compute volume series over time intervals
        metrics_over_time = (
            queryset.annotate(day=TruncDay('timestamp'))
            .values('day')
            .annotate(count=Count('id'))
            .order_by('day')
        )

        # Aggregation of events distribution
        event_breakdown = (
            queryset.values('event_name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response({
            "time_series": list(metrics_over_time),
            "breakdown": list(event_breakdown),
            "total_events": queryset.count()
        }, status=status.HTTP_200_OK)