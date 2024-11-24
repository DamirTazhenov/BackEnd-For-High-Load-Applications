from rest_framework import serializers
from .models import User, EmailConfirmation, UserProfile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken

from tasks.tasks import send_email_task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'address', 'social_security_number', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_social_security_number(self, value):
        if not value.replace("-", "").isdigit():
            raise serializers.ValidationError("Invalid Social Security Number.")
        return value


# Serializer for User Registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        # Create EmailConfirmation instance
        email_confirmation = EmailConfirmation.objects.create(user=user)

        # Send confirmation email
        send_email_task.delay(
            subject="Email Confirmation",
            message=f"Your confirmation code is {email_confirmation.confirmation_code}",
            recipient_list=[user.email],
        )
        return user


# Serializer for JWT Token
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
