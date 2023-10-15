from rest_framework import serializers
from .models import GivenToken

class GTokenSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = GivenToken
        fields = '__all__'
