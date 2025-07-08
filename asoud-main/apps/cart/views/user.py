from rest_framework import views, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from utils.response import ApiResponse
from apps.cart.models import (
    Order,
    OrderItem
)
from apps.cart.serializers.user import(
    OrderSerializer,
    Order2Serializer,
    OrderItem2Serializer,
    OrderCreateSerializer,
    OrderCheckOutSerializer,
    OrderItemSerializer,
    OrderItemUpdateSerializer
)
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_order(self, request):
        """Helper method to get or create order"""
        return Order.get_or_create_order(request.user)
    
    def list(self, request):
        """Get order contents"""
        order = self.get_order(request)
        print('order', order)
        serializer = Order2Serializer(order)
        return Response(serializer.data)
    
    def add_item(self, request):
        """Add item to cart"""
        order = self.get_order(request)
        serializer = OrderItem2Serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product', None)
        product_name = serializer.validated_data.get('product_name', None)
        affiliate = serializer.validated_data.get('affiliate', None)
        affiliate_name = serializer.validated_data.get('affiliate_name', None)
        quantity = serializer.validated_data.get('quantity', None)
        if product:
            if existing_product := order.items.filter(product=product).first():
                existing_product.quantity += quantity
                existing_product.save()
                serializer = OrderItem2Serializer(existing_product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif product_name:
            if existing_product := order.items.filter(product__name=product_name).first():
                existing_product.quantity += quantity
                existing_product.save()
                serializer = OrderItem2Serializer(existing_product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.save(order=order), status=status.HTTP_201_CREATED)
        if affiliate:
            if existing_affiliate := order.items.filter(affiliate=affiliate).first():
                existing_affiliate.quantity += quantity
                existing_affiliate.save()
                serializer = OrderItem2Serializer(existing_affiliate) 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif affiliate_name:
            if existing_affiliate := order.items.filter(affiliate__name=affiliate_name).first():
                existing_affiliate.quantity += quantity
                existing_affiliate.save()
                serializer = OrderItem2Serializer(existing_affiliate)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.save(order=order), status=status.HTTP_201_CREATED)
           
    def update_item(self, request, pk=None):
        """Update item quantity in cart"""
        order = self.get_order(request)
        try:
            item = order.items.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response(
                {"error": "Item not found in order"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
        serializer = OrderItemUpdateSerializer(
            item, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()  # No need to pass order since it's already set
    
        return Response(serializer.data)
    
    def remove_item(self, request, pk=None):
        """Remove item from order"""
        order = self.get_order(request)
        try:
            item = order.items.get(pk=pk)
            item.delete()
            serializer = Order2Serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response(
                {"error": "Item not found in order"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
    def checkout(self, request):
        order = self.get_order(request)
        serializer = OrderCheckOutSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Check if item already exists in cart
        if not order.items.exists():
            return Response(
                {"error": "order is empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = Order.PENDING 
        order.description = serializer.validated_data.get('description', 'Order placed')
        order.type = serializer.validated_data.get('type', Order.ONLINE)
        order.save()

        serializer = Order2Serializer(order)
        return Response(
            {"message": "Order placed successfully", "order": serializer.data},
            status=status.HTTP_200_OK
        )

class OrderCreateView(views.APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = serializer.save(user=request.user)
        
        if obj.items.first().product:
            user_id = obj.items.first().product.market.user.id
        else:
            user_id = obj.items.first().affiliate.market.user.id

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_notification",
                "data": {
                    "type": "order",
                    "message": "New Order Added",
                    "order": {
                        "id": str(obj.id),
                    },
                }
            }
        )

        serialized_data = OrderSerializer(obj).data

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serialized_data
            )
        )

class OrderListView(views.APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)

        serializer = OrderSerializer(orders, many=True)
        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )

class OrderDetailView(views.APIView):
    def get(self, request, pk:str):
        try:
            order = Order.objects.get(id=pk)

            serializer = OrderSerializer(order)
            return Response(
                ApiResponse(
                    success=True,
                    code=200,
                    data=serializer.data
                )
            )
        
        except Exception as e:
            return Response(
                ApiResponse(
                    success=False,
                    code=500,
                    error=str(e)
                )
            )

class OrderUpdateView(views.APIView):
    def put(self, request, pk:str):
        try:
            order = Order.objects.get(id=pk)

            serializer = OrderCreateSerializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            obj = serializer.save(user=request.user)

            if obj.items.first().product:
                user_id = obj.items.first().product.market.user.id
            else:
                user_id = obj.items.first().affiliate.market.user.id

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{user_id}",
                {
                    "type": "send_notification",
                    "data": {
                        "type": "order",
                        "message": "An Order Updated",
                        "order": {
                            "id": str(obj.id),
                        },
                    }
                }
            )

            serialized_data = OrderSerializer(obj).data

            return Response(
                ApiResponse(
                    success=True,
                    code=200,
                    data=serialized_data
                )
            )
        except Exception as e:
            return Response(
                ApiResponse(
                    success=False,
                    code=500,
                    error=str(e)
                )
            )

class OrderDeleteView(views.APIView):
    def delete(self, request, pk:str):
        try:
            order = Order.objects.get(id=pk)

            order.delete()
        
            return Response(
                ApiResponse(
                    success=True,
                    code=204,
                )
            )
        
        except Exception as e:
            return Response(
                ApiResponse(
                    success=False,
                    code=500,
                    error=str(e)
                )
            )
