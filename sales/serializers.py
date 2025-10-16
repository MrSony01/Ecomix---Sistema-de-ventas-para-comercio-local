from rest_framework import serializers
from .models import Sale, SaleItem
from inventory.models import Product

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = '__all__'
        read_only_fields = ['sale', 'subtotal', 'total']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    cashier_name = serializers.CharField(source='cashier.username', read_only=True)
    
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ['sale_number', 'created_at', 'updated_at']

class SaleListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    cashier_name = serializers.CharField(source='cashier.username', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'sale_number', 'customer', 'customer_name', 'cashier_name', 'total', 'payment_method', 'status', 'created_at']

class SaleCreateSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    
    class Meta:
        model = Sale
        fields = ['customer', 'payment_method', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        cashier = self.context['request'].user
        
        # Calculate totals
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items_data)
        discount = sum(item.get('discount', 0) for item in items_data)
        total = subtotal - discount
        
        # Create sale
        sale = Sale.objects.create(
            cashier=cashier,
            subtotal=subtotal,
            discount=discount,
            total=total,
            **validated_data
        )
        
        # Create sale items and update inventory
        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Check stock
            if product.stock < quantity:
                raise serializers.ValidationError(f"Stock insuficiente para {product.name}")
            
            # Update product stock
            product.stock -= quantity
            product.save()
            
            # Create sale item
            SaleItem.objects.create(sale=sale, **item_data)
        
        # Update customer loyalty points if customer exists
        if sale.customer:
            points_earned = int(total / 10)  # 1 point per $10
            sale.customer.loyalty_points += points_earned
            sale.customer.total_purchases += total
            sale.customer.save()
            
            from loyalty.models import LoyaltyTransaction
            LoyaltyTransaction.objects.create(
                customer=sale.customer,
                transaction_type='earn',
                points=points_earned,
                sale=sale,
                description=f"Puntos ganados por compra {sale.sale_number}",
                previous_balance=sale.customer.loyalty_points - points_earned,
                new_balance=sale.customer.loyalty_points
            )
        
        return sale
