from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail


from .models import User, Profile, ResetToken
from .serializers import (
    UserSerializer,
    ResetPasswordSerializer,
    ProfileSerializer,
    FindAccount,
)
from .utils import (
    _create_user_profile,
    _login,
    _logout,
    _reset_password,
    _reset_password_confirmation,
    _update_profile,
)

# Create your views here.


# Create/Register User View
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        return _create_user_profile(request)


# Login
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return _login(request)


# Logout
class UserLogoutView(APIView):
    def post(self, request):
        return _logout(request)


# Find Account for Reset View
class ResetPasswordView(CreateAPIView):
    serializer_class = FindAccount
    permission_classes = [AllowAny]

    def create(self, request):
        return _reset_password(self, request)


# Reset Password
class ResetPasswordConfirmationView(ListCreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def list(self, request, token):
        if ResetToken.validate_reset_token(token):
            return Response()
        else:
            return Response("Link has expired", status=status.HTTP_408_REQUEST_TIMEOUT)

    def create(self, request, token):
        return _reset_password_confirmation(self, request, token)


# Profile Viewsets
class ProfileViewsets(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def create(self, request):
        return Response("Method Not Allowed", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return _update_profile(self, request, *args, *kwargs)

    def destroy(self, request, *args, **kwargs):
        profile = self.get_object()
        profile.user.delete()
        profile.delete()
        return Response(
            "Account has been deleted successfully", status=status.HTTP_204_NO_CONTENT
        )
