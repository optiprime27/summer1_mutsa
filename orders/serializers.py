from rest_framework import serializers
from .models import Order, Order_Item
from items.serializers import ItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(source='item.id')
    count = serializers.IntegerField()

    class Meta:
        model = Order_Item
        fields = ['item_id', 'count']

class OrderSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source='member.id')
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['id', 'member_id', 'items', 'order_date', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        member_id = validated_data.pop('member_id')
        order = Order.objects.create(member_id=member_id, status='주문성공', **validated_data)

        for item_data in items_data:
            Order_Item.objects.create(order=order, item_id=item_data['item_id'], count=item_data['count'])
        
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        if items_data:
            Order_Item.objects.filter(order=instance).delete()
            for item_data in items_data:
                Order_Item.objects.create(order=instance, item_id=item_data['item_id'], count=item_data['count'])

        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
