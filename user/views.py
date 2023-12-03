from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.utils import jwt_encode
from django.http import Http404
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User
from user.serializers import UserSerializer


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data.get('email')

        if email is None:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IsAnonymousOrAutoLoginFalse(BasePermission):
    message = "Authenticated users cannot auto login."

    def has_permission(self, request, view):
        auto_login = request.data.get("auto_login", True)
        return not auto_login or request.user.is_anonymous


class JWTRegisterView(RegisterView):
    permission_classes = [IsAnonymousOrAutoLoginFalse]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED and self.auto_login:
            self.set_token_cookies(response)
        return response

    def set_token_cookies(self, response):
        if self.access_token and self.refresh_token:
            response.set_cookie(
                api_settings.JWT_AUTH_COOKIE, self.access_token, httponly=True
            )
            response.set_cookie(
                api_settings.JWT_AUTH_REFRESH_COOKIE, self.refresh_token, httponly=True
            )

    @property
    def auto_login(self):
        return self.request.data.get("auto_login", True)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        self.access_token, self.refresh_token = (
            jwt_encode(user) if self.auto_login else (None, None)
        )
        return user
