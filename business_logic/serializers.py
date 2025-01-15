from rest_framework import serializers
from .models import Dish, Order, OrderItem

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']

class OrderItemSerializer(serializers.ModelSerializer):
    dish = DishSerializer()

    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity', 'item_total']

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'status', 'created_at', 'total_price', 'orderitems']

    def get_total_price(self, obj):
        return obj.total_price()