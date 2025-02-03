from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    oauth_id_42 = models.CharField(
        max_length=255,
        null=True,
    )
    oauth_id_github = models.CharField(
        max_length=255,
        null=True,
    )
    avatar = models.FileField(null=True, upload_to='avatars/')