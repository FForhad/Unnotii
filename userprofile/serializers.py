from rest_framework import serializers
from .models import Profile, RechargeLog

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Profile
        fields = '__all__'

class RechargeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechargeLog
        fields = '__all__'

class RechargeSerializer(serializers.Serializer):
    dial_code = serializers.CharField(max_length=15)

class PaidPointSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    point = serializers.IntegerField()