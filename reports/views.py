from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg, F
from datetime import datetime, timedelta
from .models import Report
from .serializers import ReportSerializer
from sales.models import Sale
from inventory.models import Product
from loyalty.models import Customer

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['report_type']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate_sales_report(self, request):
        date_from = datetime.strptime(request.data.get('date_from'), '%Y-%m-%d').date()
        date_to = datetime.strptime(request.data.get('date_to'), '%Y-%m-%d').date()
        
        sales = Sale.objects.filter(
            created_at__date__gte=date_from,
            created_at__date__lte=date_to,
            status='completed'
        )
        
        report_data = {
            'total_sales': sales.aggregate(total=Sum('total'))['total'] or 0,
            'transaction_count': sales.count(),
            'average_sale': sales.aggregate(avg=Avg('total'))['avg'] or 0,
            'payment_methods': sales.values('payment_method').annotate(
                total=Sum('total'),
                count=Count('id')
            ),
            'top_products': sales.values('items__product__name').annotate(
                quantity=Sum('items__quantity'),
                total=Sum('items__total')
            ).order_by('-total')[:10]
        }
        
        report = Report.objects.create(
            name=f"Reporte de Ventas {date_from} - {date_to}",
            report_type='sales',
            date_from=date_from,
            date_to=date_to,
            generated_by=request.user,
            data=report_data
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_inventory_report(self, request):
        date_from = datetime.strptime(request.data.get('date_from'), '%Y-%m-%d').date()
        date_to = datetime.strptime(request.data.get('date_to'), '%Y-%m-%d').date()
        
        products = Product.objects.filter(is_active=True)
        
        report_data = {
            'total_products': products.count(),
            'low_stock_products': products.filter(stock__lte=F('min_stock')).count(),
            'total_inventory_value': sum(p.stock * p.cost for p in products),
            'products_by_category': products.values('category__name').annotate(
                count=Count('id'),
                total_value=Sum(F('stock') * F('cost'))
            )
        }
        
        report = Report.objects.create(
            name=f"Reporte de Inventario {date_from} - {date_to}",
            report_type='inventory',
            date_from=date_from,
            date_to=date_to,
            generated_by=request.user,
            data=report_data
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def generate_customer_report(self, request):
        date_from = datetime.strptime(request.data.get('date_from'), '%Y-%m-%d').date()
        date_to = datetime.strptime(request.data.get('date_to'), '%Y-%m-%d').date()
        
        customers = Customer.objects.filter(is_active=True)
        
        report_data = {
            'total_customers': customers.count(),
            'total_loyalty_points': customers.aggregate(total=Sum('loyalty_points'))['total'] or 0,
            'average_purchase_per_customer': customers.aggregate(avg=Avg('total_purchases'))['avg'] or 0,
            'customers_by_tier': {
                'Oro': customers.filter(total_purchases__gte=1000).count(),
                'Plata': customers.filter(total_purchases__gte=500, total_purchases__lt=1000).count(),
                'Bronce': customers.filter(total_purchases__gte=100, total_purchases__lt=500).count(),
                'Básico': customers.filter(total_purchases__lt=100).count(),
            }
        }
        
        report = Report.objects.create(
            name=f"Reporte de Clientes {date_from} - {date_to}",
            report_type='customers',
            date_from=date_from,
            date_to=date_to,
            generated_by=request.user,
            data=report_data
        )
        
        serializer = self.get_serializer(report)
        return Response(serializer.data)
