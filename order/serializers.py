from rest_framework import serializers

from order.models import Order, OrderItems


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ('product', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('products', 'notes')

    def create(self, validated_data):
        total_sum = 0
        request = self.context.get('request')
        user = request.user
        validated_data['user'] = user
        validated_data['status'] = 'new'
        validated_data['total_sum'] = 0
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for prod in products:
            total_sum += prod['product'].price * prod['quantity']
            OrderItems.objects.create(order=order, **prod)
        order.total_sum = total_sum
        order.save()
        return order