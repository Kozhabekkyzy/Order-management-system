from rest_framework import serializers
from .models import Order, Item, Status

class OrderSerializer(serializers.ModelSerializer):
    items_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Item.objects.all(), write_only=True, source='items'
    )
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(), write_only=True, source='status'
    )

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'items_ids', 'total_price', 'status_id', 'comment']
        read_only_fields = ['id', 'total_price']
