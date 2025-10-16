from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg
from datetime import datetime, timedelta
from .models import Sale, SaleItem
from .serializers import SaleSerializer, SaleListSerializer, SaleCreateSerializer, SaleItemSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'customer', 'cashier']
    search_fields = ['sale_number', 'customer__name']
    ordering_fields = ['created_at', 'total']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SaleListSerializer
        elif self.action == 'create':
            return SaleCreateSerializer
        return SaleSerializer
    
    @action(detail=False, methods=['get'])
    def today_sales(self, request):
        today = datetime.now().date()
        sales = self.queryset.filter(created_at__date=today, status='completed')
        total = sales.aggregate(total=Sum('total'))['total'] or 0
        count = sales.count()
        
        return Response({
            'date': today,
            'total_sales': total,
            'transaction_count': count,
            'average_sale': total / count if count > 0 else 0
        })
    
    @action(detail=False, methods=['get'])
    def sales_by_period(self, request):
        period = request.query_params.get('period', 'week')  # day, week, month, year
        
        if period == 'day':
            start_date = datetime.now().date()
        elif period == 'week':
            start_date = datetime.now().date() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.now().date() - timedelta(days=30)
        else:  # year
            start_date = datetime.now().date() - timedelta(days=365)
        
        sales = self.queryset.filter(created_at__date__gte=start_date, status='completed')
        total = sales.aggregate(total=Sum('total'))['total'] or 0
        count = sales.count()
        
        return Response({
            'period': period,
            'start_date': start_date,
            'end_date': datetime.now().date(),
            'total_sales': total,
            'transaction_count': count,
            'average_sale': total / count if count > 0 else 0
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        sale = self.get_object()
        
        if sale.status == 'cancelled':
            return Response({'error': 'La venta ya está cancelada'}, status=400)
        
        # Restore inventory
        for item in sale.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        # Reverse loyalty points if applicable
        if sale.customer:
            points_to_reverse = int(sale.total / 10)
            sale.customer.loyalty_points -= points_to_reverse
            sale.customer.total_purchases -= sale.total
            sale.customer.save()
        
        sale.status = 'cancelled'
        sale.save()
        
        serializer = self.get_serializer(sale)
        return Response(serializer.data)

class SaleItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sale', 'product']
