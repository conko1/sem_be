from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_employer', 'created', 'is_staff', 'is_superuser']
        read_only_fields = ['email', 'created', 'is_employer']
        extra_kwargs = {
            'first_name': {'max_length': 150},
            'last_name': {'max_length': 150},
            'email': {'required': True}
        }
