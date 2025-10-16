from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, LoyaltyTransactionViewSet, RewardViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'transactions', LoyaltyTransactionViewSet)
router.register(r'rewards', RewardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
