from django.core.management.base import BaseCommand
from users.models import User
from inventory.models import Category, Product
from loyalty.models import Customer, Reward
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos iniciales para pruebas del sistema'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos iniciales...')
        
        # Crear usuarios de prueba
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ecomix.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario admin creado'))
        
        if not User.objects.filter(username='cajero').exists():
            User.objects.create_user(
                username='cajero',
                email='cajero@ecomix.com',
                password='cajero123',
                first_name='Juan',
                last_name='Pérez',
                role='cashier'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario cajero creado'))
        
        if not User.objects.filter(username='gerente').exists():
            User.objects.create_user(
                username='gerente',
                email='gerente@ecomix.com',
                password='gerente123',
                first_name='María',
                last_name='González',
                role='manager'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario gerente creado'))
        
        # Crear categorías
        categories_data = [
            ('Bebidas', 'Bebidas frías y calientes'),
            ('Snacks', 'Snacks y golosinas'),
            ('Lácteos', 'Productos lácteos'),
            ('Panadería', 'Pan y productos de panadería'),
            ('Aseo', 'Productos de aseo personal'),
        ]
        
        for name, description in categories_data:
            if not Category.objects.filter(name=name).exists():
                Category.objects.create(name=name, description=description)
                self.stdout.write(self.style.SUCCESS(f'✓ Categoría {name} creada'))
        
        # Crear productos
        bebidas = Category.objects.get(name='Bebidas')
        snacks = Category.objects.get(name='Snacks')
        
        products_data = [
            ('Coca Cola 350ml', 'COCA-350', '7501055301274', bebidas, Decimal('2500'), Decimal('1500'), 100),
            ('Agua Cristal 600ml', 'AGUA-600', '7501055302345', bebidas, Decimal('1500'), Decimal('800'), 150),
            ('Papas Margarita 150g', 'PAP-150', '7501055303456', snacks, Decimal('3000'), Decimal('1800'), 80),
            ('Chocolatina Jet', 'CHOC-JET', '7501055304567', snacks, Decimal('1800'), Decimal('1000'), 120),
        ]
        
        for name, sku, barcode, category, price, cost, stock in products_data:
            if not Product.objects.filter(sku=sku).exists():
                Product.objects.create(
                    name=name,
                    sku=sku,
                    barcode=barcode,
                    category=category,
                    price=price,
                    cost=cost,
                    stock=stock,
                    min_stock=20
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Producto {name} creado'))
        
        # Crear clientes
        customers_data = [
            ('Carlos Rodríguez', 'carlos@example.com', '3001234567'),
            ('Ana Martínez', 'ana@example.com', '3007654321'),
            ('Luis García', 'luis@example.com', '3009876543'),
        ]
        
        for name, email, phone in customers_data:
            if not Customer.objects.filter(phone=phone).exists():
                Customer.objects.create(
                    name=name,
                    email=email,
                    phone=phone
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Cliente {name} creado'))
        
        # Crear recompensas
        rewards_data = [
            ('Descuento 5%', 'Descuento del 5% en tu próxima compra', 50),
            ('Descuento 10%', 'Descuento del 10% en tu próxima compra', 100),
            ('Descuento 15%', 'Descuento del 15% en tu próxima compra', 200),
            ('Producto Gratis', 'Un producto gratis de hasta $5000', 500),
        ]
        
        for name, description, points in rewards_data:
            if not Reward.objects.filter(name=name).exists():
                Reward.objects.create(
                    name=name,
                    description=description,
                    points_required=points
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Recompensa {name} creada'))
        
        self.stdout.write(self.style.SUCCESS('\n¡Datos iniciales cargados exitosamente!'))
        self.stdout.write(self.style.WARNING('\nCredenciales de acceso:'))
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Cajero: cajero / cajero123')
        self.stdout.write('Gerente: gerente / gerente123')
