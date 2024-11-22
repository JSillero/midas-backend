from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(max_length=5000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    follows = models.ManyToManyField(
        to='story.Story',
        related_name='user_follows',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
