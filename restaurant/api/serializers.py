from rest_framework import serializers
from restaurant.models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'open_time', 'close_time']