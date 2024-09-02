from rest_framework import serializers

from tasks.models import Task, TimeLog


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_by"]


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ["id", "task", "hours_spent", "description", "created_at"]
        read_only_fields = ["id", "user", "task", "created_at"]
