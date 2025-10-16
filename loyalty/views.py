from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer, LoyaltyTransaction, Reward
from .serializers import CustomerSerializer, CustomerListSerializer, LoyaltyTransactionSerializer, RewardSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name', 'phone', 'email']
    ordering_fields = ['name', 'loyalty_points', 'total_purchases', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    @action(detail=True, methods=['post'])
    def redeem_points(self, request, pk=None):
        customer = self.get_object()
        points = request.data.get('points', 0)
        
        if points <= 0:
            return Response({'error': 'Los puntos deben ser mayores a 0'}, status=400)
        
        if customer.loyalty_points < points:
            return Response({'error': 'Puntos insuficientes'}, status=400)
        
        previous_balance = customer.loyalty_points
        customer.loyalty_points -= points
        customer.save()
        
        LoyaltyTransaction.objects.create(
            customer=customer,
            transaction_type='redeem',
            points=points,
            description=request.data.get('description', 'Redención de puntos'),
            previous_balance=previous_balance,
            new_balance=customer.loyalty_points
        )
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)

class LoyaltyTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoyaltyTransaction.objects.all()
    serializer_class = LoyaltyTransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'transaction_type']
    ordering_fields = ['created_at']

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['name']
    ordering_fields = ['points_required', 'name']
