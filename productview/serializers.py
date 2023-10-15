from rest_framework import serializers
from .models import ProductItem, ProductPoint

class ProductItemSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductItem
        fields = '__all__'
    
class ProductPointSerializer(serializers.ModelSerializer):
    #user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductPoint
        fields = '__all__'

