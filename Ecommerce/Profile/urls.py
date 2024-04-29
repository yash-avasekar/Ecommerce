from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# URLS

router = DefaultRouter()
router.register("", views.ProfileViewsets)

urlpatterns = [
    path("register-user/", views.CreateUserView.as_view()),
    path("login/", views.UserLoginView.as_view()),
    path("logout/", views.UserLogoutView.as_view()),
    #
    path("reset-password/", views.ResetPasswordView.as_view()),
    path(
        f"reset-password/<uuid:token>/", views.ResetPasswordConfirmationView.as_view()
    ),
    #
    path("profile/", include(router.urls)),
]
