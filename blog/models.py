from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

class Level(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=11, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Blog(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(Level, models.CASCADE,blank=True, null=True)
    lecturer = models.ForeignKey(User, models.PROTECT, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title