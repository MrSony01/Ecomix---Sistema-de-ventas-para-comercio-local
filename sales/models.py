from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from inventory.models import Product

class Sale(models.Model):
    """
    Sales transaction model for POS
    """
    PAYMENT_METHODS = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta'),
        ('transfer', 'Transferencia'),
    ]
    
    STATUS_CHOICES = [
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('pending', 'Pendiente'),
    ]
    
    sale_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey('loyalty.Customer', on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    cashier = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='sales')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Venta {self.sale_number} - ${self.total}"
    
    def save(self, *args, **kwargs):
        if not self.sale_number:
            # Generate sale number
            import datetime
            prefix = datetime.datetime.now().strftime('%Y%m%d')
            last_sale = Sale.objects.filter(sale_number__startswith=prefix).order_by('-sale_number').first()
            if last_sale:
                last_number = int(last_sale.sale_number[-4:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.sale_number = f"{prefix}{new_number:04d}"
        super().save(*args, **kwargs)


class SaleItem(models.Model):
    """
    Individual items in a sale
    """
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    class Meta:
        verbose_name = 'Item de Venta'
        verbose_name_plural = 'Items de Venta'
        
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        self.total = self.subtotal - self.discount
        super().save(*args, **kwargs)
