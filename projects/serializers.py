from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["user"]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise ValidationError({"name": "A project with this name already exists."})


class AddMembersSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, required=True
    )

    class Meta:
        model = Project
        fields = ["members"]

    def update(self, instance, validated_data):
        members = validated_data.get("members", [])
        instance.members.set(members)  # Add members to the project
        instance.save()
        return instance
