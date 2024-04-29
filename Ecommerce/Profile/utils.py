from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings

from .models import User, Profile, ResetToken
from .serializers import UserSerializer


def sendMail(email, subject, message):
    try:
        send_mail(
            from_email=settings.EMAIL_FROM,
            recipient_list=[email],
            subject=subject,
            message=message,
            fail_silently=True,
        )
        return True
    except:
        return False


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _create_user_profile(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username, email, password, confirm_password = (
        serializer.validated_data["username"],  # type: ignore
        serializer.validated_data["email"],  # type: ignore
        serializer.validated_data["password"],  # type: ignore
        serializer.validated_data["confirm_password"],  # type: ignore
    )

    if email is None or email == "":
        return Response("Email field is required")

    if password != confirm_password:
        return Response("Password doesn't matches")

    user = User.objects.create_user(username=username, email=email, password=password)
    if user:
        Profile.objects.create(user=user, username=user.username, email=user.email)
        user.save()
        subject = "Welcome to [Your Application Name]!"
        message = f"""
Dear {user.username},

Thank you for registering with [Ecommerce Application]! We're excited to have you on board.

Your account has been successfully created. You can now log in using the username and password you provided during registration.

If you have any questions or need assistance, please don't hesitate to contact us at [Your Support Email].

Best regards,
[Ecommerce Team]
"""
        sendMail(email=user.email, subject=subject, message=message)
        return Response("User Registered Successfully", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _login(request):
    username, password = request.data["username"], request.data["password"]
    user = authenticate(request, username=username, password=password)

    if user is None:
        return Response("Invalid Username or Password")

    login(request, user)
    token, created = Token.objects.get_or_create(user=user)
    data = {"Token ": token.key}

    return Response(data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _logout(request):
    Token.objects.get(user=request.user).delete()
    logout(request)
    return Response("User Logged Out", status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _reset_password(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]  # type: ignore

    # Find if account exists
    try:
        user = User.objects.get(email=email)
    except:
        return Response(
            "Email you entered is not registered", status=status.HTTP_200_OK
        )

    token = ResetToken.get_or_create_token(user=user)
    subject = "Password Reset Request"
    message = f"""
Dear {user.email},

We have received a request to reset the password associated with your account. To ensure the security of your account, please follow the steps below to reset your password:


Click on the "Reset Password" link.
Enter requried data accociated with it

http://localhost:8000/api/user/reset-password/{token}/

Check your email inbox for further instructions.

If you did not initiate this request, please disregard this message. Your account security is important to us, and we recommend that you change your password periodically to maintain its integrity.

Thank you for your attention to this matter.

Best regards,
[Your Company Name] 
    """

    sendMail(user.email, subject, message)

    return Response(
        "Password Reset Link Was Send To Your Registered Email Address",
        status=status.HTTP_200_OK,
    )


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _reset_password_confirmation(self, request, token):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    new_password, confirm_password = (
        serializer.validated_data["new_password"],
        serializer.validated_data["confirm_password"],
    )

    if not ResetToken.validate_reset_token(token):
        return Response("Link has expired", status=status.HTTP_408_REQUEST_TIMEOUT)

    try:
        user_obj = ResetToken.get_queryset(token)
        user = User.objects.get(username=user_obj.user.username)
    except Exception as e:
        return Response("User Account not found", status=status.HTTP_400_BAD_REQUEST)

    if new_password != confirm_password:
        return Response("Password does not matches", status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    subject = "Password Changed"
    message = f"""
Dear {request.user.username},

You are receiving this email because your password for your account with [Ecommerce App] has been changed successfully.

If you did not request this change, please contact our support team immediately.

If you have any questions or need assistance, please contact us at [Your Support Email].

Best regards,

[Your Application Team]
"""
    send_mail(
        from_email=settings.EMAIL_FROM,
        recipient_list=[user.email],
        subject=subject,
        message=message,
    )
    return Response("Password has been updated", status=status.HTTP_201_CREATED)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------


def _update_profile(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance=instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)

    user = instance.user
    user.username = serializer.validated_data.get("username", instance.username)
    user.email = serializer.validated_data.get("email", instance.email)
    user.first_name = serializer.validated_data.get("first_name", instance.first_name)
    user.last_name = serializer.validated_data.get("last_name", instance.email)

    user.save()

    if (
        instance.email != serializer.validated_data["email"]
        or instance.username != serializer.validated_data["username"]
    ):

        subject = (
            "Email has been updated"
            if instance.email != serializer.validated_data["email"]
            else "Username has updated"
        )

        message = ""
        if subject == "Username has updated":
            message += (
                f"{subject} to '{serializer.validated_data['username']}' successfully"
            )
        else:
            message += (
                f"{subject} to '{serializer.validated_data['email']}' successfully"
            )

        message += "\nIf you did not make these changes or believe this is an error, please contact our support team immediately.\n"
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_FROM,
            recipient_list=[serializer.validated_data["email"]],
        )

    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
