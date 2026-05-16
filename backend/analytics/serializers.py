from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from analytics.models import Organization, User, Event

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = cls.get_token(user)
        # Inject custom tenant claims into JWT payload for high performance injection
        token['org_id'] = str(user.organization.id) if user.organization else None
        token['role'] = user.role
        return token

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'