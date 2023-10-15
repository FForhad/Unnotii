from rest_framework import serializers
from .models import Code

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class RechargeSerializer(serializers.Serializer):
    dial_code = serializers.CharField(max_length=15)


class PaidPointSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    point = serializers.IntegerField()