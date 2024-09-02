import uuid

from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # TODO remove default
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='projects', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title
