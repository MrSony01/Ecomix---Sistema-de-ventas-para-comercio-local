from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Category, Product, StockMovement
from users.models import User

class InventoryAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            role='admin'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Bebidas',
            description='Bebidas frías y calientes'
        )
        
        self.product = Product.objects.create(
            name='Coca Cola',
            sku='COCA-001',
            category=self.category,
            price=Decimal('2500'),
            cost=Decimal('1500'),
            stock=100
        )
    
    def test_list_categories(self):
        """Test listing categories"""
        response = self.client.get('/api/inventory/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_product(self):
        """Test creating a product"""
        data = {
            'name': 'Pepsi',
            'sku': 'PEPSI-001',
            'category': self.category.id,
            'price': '2500',
            'cost': '1500',
            'stock': 50
        }
        response = self.client.post('/api/inventory/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_stock_movement(self):
        """Test stock movement"""
        data = {
            'product': self.product.id,
            'movement_type': 'in',
            'quantity': 50,
            'reason': 'Compra a proveedor'
        }
        response = self.client.post('/api/inventory/stock-movements/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check stock updated
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 150)
