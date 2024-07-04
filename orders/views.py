from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def cancel(self, request, pk=None):
        try:
            order = self.get_object()
            order.status = '주문취소'
            return Response({'id': order.id, 'status': order.status}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def member_orders(self, request):
        member_id = request.query_params.get('member_id')
        if not member_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        orders = Order.objects.filter(member_id=member_id)
        orders_data = [
            {
                'id': order.id,
                'order_date': order.order_date,
                'status': order.status
            }
            for order in orders
        ]
        return Response({'member_id': member_id, 'orders': orders_data}, status=status.HTTP_200_OK)
