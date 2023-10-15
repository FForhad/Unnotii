from rest_framework import serializers
from .models import CustomUser, OTP

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'phone_number', 'first_name', 'last_name', 'is_verified')

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('id', 'user', 'otp', 'created_at')
