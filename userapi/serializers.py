# This files contains UserSerializer and ActivitySerilizer
# which are used to simplify the rendering of complex querysets into JSON

from rest_framework import serializers
from .models import User, ActivityPeriod


class ActivityPeriodSerializer(serializers.ModelSerializer):
    """ Serializes ActivityPeriod queryset."""
    # Re-formats the start_time from db into human readable datetime
    start_time = serializers.DateTimeField(format="%b %d %Y %H:%M %p", read_only=True)
    # Re-formats the end_time from db into human readable datetime
    end_time = serializers.DateTimeField(format="%b %d %Y %H:%M %p", read_only=True)

    class Meta:
        model = ActivityPeriod
        fields = ["start_time", "end_time"]


class UserSerializer(serializers.ModelSerializer):
    """ Serializes  User queryset."""
    # Establishes relationship between UserSerializer and ActivitySerializer
    # therefore creating a nested serializer with corresponding ActivtyPeriod records inside the User record
    activity_periods = ActivityPeriodSerializer(many=True, read_only=True, source="activity_period")

    class Meta:
        model = User
        fields = ['id', 'real_name', 'tz', 'activity_periods']
