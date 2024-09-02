from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), required=False
    )

    def save(self, request):
        user = super().save(request)
        group = self.validated_data.get("group")
        if group:
            user.groups.add(group)
        return user


class CustomLoginSerializer(LoginSerializer):
    username = None

    email = serializers.EmailField(required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        attrs["user"] = user
        return attrs
