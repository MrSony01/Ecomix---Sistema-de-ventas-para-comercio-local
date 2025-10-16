from django.contrib import admin
from .models import Customer, LoyaltyTransaction, Reward

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'loyalty_points', 'membership_tier', 'total_purchases', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'transaction_type', 'points', 'previous_balance', 'new_balance', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['customer__name', 'description']
    readonly_fields = ['created_at']

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ['name', 'points_required', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
