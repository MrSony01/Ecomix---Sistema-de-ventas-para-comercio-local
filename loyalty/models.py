from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Customer(models.Model):
    """
    Customer model for loyalty program
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField(blank=True, null=True)
    loyalty_points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.00'))])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    @property
    def membership_tier(self):
        """Calculate customer membership tier based on total purchases"""
        if self.total_purchases >= 1000:
            return 'Oro'
        elif self.total_purchases >= 500:
            return 'Plata'
        elif self.total_purchases >= 100:
            return 'Bronce'
        return 'Básico'


class LoyaltyTransaction(models.Model):
    """
    Track loyalty points transactions
    """
    TRANSACTION_TYPES = [
        ('earn', 'Ganados'),
        ('redeem', 'Redimidos'),
        ('adjust', 'Ajuste'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loyalty_transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    points = models.IntegerField(validators=[MinValueValidator(1)])
    sale = models.ForeignKey('sales.Sale', on_delete=models.SET_NULL, null=True, blank=True, related_name='loyalty_transactions')
    description = models.CharField(max_length=200)
    previous_balance = models.IntegerField()
    new_balance = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Transacción de Puntos'
        verbose_name_plural = 'Transacciones de Puntos'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.customer.name} - {self.get_transaction_type_display()} - {self.points} pts"


class Reward(models.Model):
    """
    Rewards that can be redeemed with loyalty points
    """
    name = models.CharField(max_length=200)
    description = models.TextField()
    points_required = models.IntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Recompensa'
        verbose_name_plural = 'Recompensas'
        ordering = ['points_required']
        
    def __str__(self):
        return f"{self.name} - {self.points_required} pts"
