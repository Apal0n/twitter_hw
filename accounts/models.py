from django.db import models
from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# User = get_user_model()


def profile_image_store(instance, filename):
    return f"profile/{instance.username}/{filename}"


class User(AbstractUser):
    profile_image = models.ImageField(upload_to=profile_image_store, default='profile/default.png')

    def __str__(self):
        return self.username


class Profile(models.Model):
    phone_number = models.CharField(max_length=13)
    short_info = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

