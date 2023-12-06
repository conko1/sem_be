from rest_framework import serializers

from user.models import User
from .models import Event, EventType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'user': {'required': True},
            'type': {'required': True}
        }
        depth = 1

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        error_messages={
            'does_not_exist': 'User does not exist.',
            'incorrect_type': 'Invalid type. Expected a user ID.',
        }
    )

    type = serializers.PrimaryKeyRelatedField(
        queryset=EventType.objects.all(),
        error_messages={
            'does_not_exist': 'Type does not exist.',
            'incorrect_type': 'Invalid type. Expected a event type ID.',
        }
    )


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'
        extra_kwargs = {
            'created': {'read_only': True},
            'key': {'required': True},
            'description': {'required': True}
        }
