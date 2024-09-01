import uuid

from django.db import models

from projects.models import Project

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_id = models.ForeignKey(Project, related_name='projects', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title