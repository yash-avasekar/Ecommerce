from datetime import timedelta
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="Profile")
    username = models.CharField(null=False, blank=False, max_length=150, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    address = models.TextField(null=True, blank=True)
    state = models.CharField(null=True, blank=True, max_length=50)
    city = models.CharField(null=True, blank=True, max_length=50)
    zipcode = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        validators=[MinLengthValidator(6), MaxLengthValidator(6)],
    )
    landmark = models.CharField(null=True, blank=True, max_length=255)
    contact_no = models.CharField(
        null=True,
        blank=True,
        max_length=10,
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
    )
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.username if self.username else self.first_name


# Reset Token
class ResetToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expiration_time = models.DateTimeField()

    def __str__(self):
        return str(self.user.username)

    @classmethod
    def get_queryset(cls, token):
        return ResetToken.objects.get(token=token)

    @classmethod
    def get_or_create_token(cls, user=None):
        expire = timezone.now() + timedelta(minutes=10)
        try:
            user = cls.objects.get(user=user)
            if cls.validate_reset_token(user.token):
                pass
            return user.token
        except:
            reset_token = cls.objects.create(user=user, expiration_time=expire)
            return reset_token.token

    @classmethod
    def validate_reset_token(cls, token):
        try:
            reset_token = cls.objects.get(token=token)  # if key present
            if reset_token.expiration_time >= timezone.now():  # if token time out
                return True
            reset_token.delete()
            return False
        except Exception as e:  # if key is not peresent
            print(e)
            return False
