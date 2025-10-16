from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Producto, Venta, ItemVenta
from .serializers import ProductoSerializer, VentaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    @action(detail=False, methods=['get'])
    def con_stock_bajo(self, request):
        """Productos con stock menor a 5 unidades"""
        productos = Producto.objects.filter(stock__lt=5)
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    
    def create(self, request):
        """Procesar una nueva venta"""
        try:
            data = request.data
            print("Datos recibidos:", data)  # Para debug
            
            # Crear la venta
            venta = Venta.objects.create(total=data['total'])
            
            # Crear items de la venta y actualizar stock
            for item in data['items']:
                producto = Producto.objects.get(id=item['producto_id'])
                
                # Crear item de venta
                ItemVenta.objects.create(
                    venta=venta,
                    producto=producto,
                    cantidad=item['cantidad'],
                    precio=item['precio']
                )
                
                # Actualizar stock del producto
                producto.stock -= item['cantidad']
                producto.save()
            
            return Response({
                'id': venta.id, 
                'mensaje': 'Venta procesada correctamente',
                'total': venta.total
            }, status=status.HTTP_201_CREATED)
            
        except Producto.DoesNotExist:
            return Response({
                'error': 'Producto no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': f'Error al procesar venta: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)
