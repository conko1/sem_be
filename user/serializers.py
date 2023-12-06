from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.core.exceptions import ValidationError
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'is_employer', 'created', 'is_staff']
        read_only_fields = ['email', 'created', 'is_employer', 'is_staff']
        extra_kwargs = {
            'first_name': {'max_length': 150},
            'last_name': {'max_length': 150},
            'email': {'required': True, 'max_length': 254}
        }


class UserRegisterSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(
        max_length=User._meta.get_field("first_name").max_length,
        validators=User._meta.get_field("first_name").validators,
    )
    last_name = serializers.CharField(
        max_length=User._meta.get_field("last_name").max_length,
        validators=User._meta.get_field("last_name").validators,
    )
    password1 = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    auto_login = serializers.BooleanField(default=True)

    def validate_email(self, email):
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Email has been already registered."
            )
        return email

    def validate(self, data):
        if data.get("password1") or data.get("password2"):
            if data.get("password1") != data.get("password2"):
                raise serializers.ValidationError(
                    "The two password fields didn't match."
                )
        return data

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data["first_name"] = self.validated_data.get("first_name", "")
        cleaned_data["last_name"] = self.validated_data.get("last_name", "")
        cleaned_data["auto_login"] = self.validated_data.get("auto_login", True)
        return cleaned_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user = adapter.save_user(request, user, self, commit=False)

        if "password1" in self.cleaned_data and self.cleaned_data["password1"]:
            try:
                adapter.clean_password(self.cleaned_data["password1"], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        else:
            user.set_unusable_password()

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
