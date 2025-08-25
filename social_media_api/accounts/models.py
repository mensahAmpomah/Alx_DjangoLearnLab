from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    # Users that this user follows (explicit field, as requested)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers_set',
        blank=True
    )

    def __str__(self):
        return self.username