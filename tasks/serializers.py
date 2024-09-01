from rest_framework import serializers

from tasks.models import Task, TimeLog

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ['id', 'task', 'hours_spent', 'description', 'logged_at']
        read_only_fields = ['id', 'logged_at']