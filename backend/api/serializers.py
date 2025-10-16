from rest_framework import serializers
from .models import Producto, Venta, ItemVenta

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'codigo', 'nombre', 'precio', 'stock', 'imagen']

class ItemVentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = ItemVenta
        fields = ['id', 'producto', 'producto_nombre', 'cantidad', 'precio']

class VentaSerializer(serializers.ModelSerializer):
    items = ItemVentaSerializer(many=True, read_only=True)
    
    class Meta:
        model = Venta
        fields = ['id', 'fecha', 'total', 'items']