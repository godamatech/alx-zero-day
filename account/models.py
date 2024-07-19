from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    level = models.ForeignKey('blog.level', models.PROTECT, null=True, blank=True)
