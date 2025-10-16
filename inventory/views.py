from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, StockMovement
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer, StockMovementSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku', 'barcode']
    ordering_fields = ['name', 'price', 'stock', 'created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = self.queryset.filter(stock__lte=models.F('min_stock'))
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['product', 'movement_type']
    search_fields = ['product__name', 'reason']
    ordering_fields = ['created_at']
    
    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        movement_type = serializer.validated_data['movement_type']
        quantity = serializer.validated_data['quantity']
        
        previous_stock = product.stock
        
        if movement_type == 'in':
            new_stock = previous_stock + quantity
        elif movement_type == 'out':
            new_stock = previous_stock - quantity
        else:  # adjust
            new_stock = quantity
        
        product.stock = new_stock
        product.save()
        
        serializer.save(
            created_by=self.request.user,
            previous_stock=previous_stock,
            new_stock=new_stock
        )
