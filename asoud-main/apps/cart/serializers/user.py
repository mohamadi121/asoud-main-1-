from rest_framework import serializers
from apps.cart.models import (
    Order, 
    OrderItem
)
from apps.product.models import Product
from apps.affiliate.models import AffiliateProduct
from django.db import transaction


class OrderItem2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'affiliate',
            'quantity'
        )
    # price = serializers.SerializerMethodField()
    # total_price = serializers.SerializerMethodField()
    # def get_price(self, obj):
    #     if obj.product:
    #         print("PRICE", obj.product.price)
    #         return obj.product.price
    #     elif obj.affiliate:
    #         print("PRICE1", obj.product.price)
    #         return obj.affiliate.price
    #     return 0
    
    # def get_total_price(self, obj):
    #     print("total_price", obj.product.price)
    #     return obj.total_price()
    
    # def get_product(self, obj):
        
    # def get_product(self, obj):
    #     print("###", obj)
    #     if obj.product:
    #         return obj.product.name
    #     elif obj.affiliate:
    #         return obj.affiliate.name
    #     return "unknown"

class Order2Serializer(serializers.ModelSerializer):
    items = OrderItem2Serializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
    
    def get_total_price(self, obj):
        return obj.total_price()
    
    def get_total_items(self, obj):
        return obj.total_items()
    

class OrderCheckOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'description', 
            'type',
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [
            'product_name', 
            'quantity'
        ]

    def get_product_name(self, obj):
        if obj.product:
            return obj.product.name
        elif obj.affiliate:
            return obj.affiliate.name
        return "unknown"

class OrderItemCreateSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    class Meta:
        model = OrderItem
        fields = [
            'product_id', 
            'quantity'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = [
            'id',
            'description', 
            'created_at', 
            'is_paid',
            'total'
        ]

    def get_total(self, obj):
        return obj.total_price()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 
            'description', 
            'created_at', 
            'is_paid',
            'total',
            'type',
            'status',
            'owner_description',
            'items'
        ]
        read_only_fields = [
            'id', 
            'user', 
            'created_at', 
            'is_paid'
        ]

    def get_total(self, obj):
        return obj.total_price()
    
class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)
    description = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=['online', 'cash'])

    class Meta:
        model = Order
        fields = [
            'description', 
            'type',
            'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        order = Order.objects.create(**validated_data)
        
        # add items
        for item_data in items_data:
            
            try:
                product = Product.objects.get(id=item_data['product_id'])
            except:
                product = None
            try:
                affiliate = AffiliateProduct.objects.get(id=item_data['product_id'])
            except:
                affiliate = None
            
            if not product and not affiliate:
                order.delete()
                raise Exception('One or More Products were Not Found')
            
            OrderItem.objects.create(
                order=order, 
                product=product, 
                affiliate=affiliate,
                quantity=item_data['quantity'], 
            )
        
        return order
    

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            # If new items are provided, replace the old ones
            if items_data is not None:
                # Delete existing items
                instance.items.all().delete()

                # Add new items
                for item_data in items_data:
                    product_id = item_data.get('product_id')
                    quantity = item_data.get('quantity')

                    product = None
                    affiliate = None

                    # Fetch product or affiliate
                    if product_id:
                        try:
                            product = Product.objects.get(id=product_id)
                        except Product.DoesNotExist:
                            pass

                        try:
                            affiliate = AffiliateProduct.objects.get(id=product_id)
                        except AffiliateProduct.DoesNotExist:
                            pass  

                    if not product and not affiliate:
                        raise serializers.ValidationError(f"Neither product nor affiliate found for id {product_id}.")

                    # Create the OrderItem
                    OrderItem.objects.create(
                        order=instance,
                        product=product,
                        affiliate=affiliate,
                        quantity=quantity
                    )

        # Save the updated Order instance
        instance.save()

        return instance
    
