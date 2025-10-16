from rest_framework import serializers
from .models import Customer, LoyaltyTransaction, Reward

class CustomerSerializer(serializers.ModelSerializer):
    membership_tier = serializers.CharField(read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'

class CustomerListSerializer(serializers.ModelSerializer):
    membership_tier = serializers.CharField(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'loyalty_points', 'membership_tier', 'total_purchases', 'is_active']

class LoyaltyTransactionSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = LoyaltyTransaction
        fields = '__all__'
        read_only_fields = ['previous_balance', 'new_balance', 'created_at']

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = '__all__'
