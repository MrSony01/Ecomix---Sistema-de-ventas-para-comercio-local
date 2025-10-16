# Documentación de la API - Ecomix

## Autenticación

Todos los endpoints (excepto login y registro) requieren autenticación JWT.

### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "contraseña"
}
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

### Usar Token
Incluir en headers:
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbG...
```

## Módulo de Usuarios

### Listar Usuarios
```http
GET /api/users/
```

### Crear Usuario
```http
POST /api/users/
Content-Type: application/json

{
  "username": "cajero1",
  "email": "cajero@example.com",
  "password": "contraseña123",
  "password2": "contraseña123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "role": "cashier",
  "phone": "3001234567"
}
```

### Obtener Usuario Actual
```http
GET /api/users/me/
```

## Módulo de Inventario

### Categorías

#### Listar Categorías
```http
GET /api/inventory/categories/
```

#### Crear Categoría
```http
POST /api/inventory/categories/
Content-Type: application/json

{
  "name": "Bebidas",
  "description": "Bebidas frías y calientes"
}
```

### Productos

#### Listar Productos
```http
GET /api/inventory/products/
```

Parámetros de consulta:
- `category`: Filtrar por categoría (ID)
- `is_active`: Filtrar por estado (true/false)
- `search`: Buscar por nombre, SKU o código de barras

#### Crear Producto
```http
POST /api/inventory/products/
Content-Type: application/json

{
  "name": "Coca Cola 350ml",
  "description": "Bebida gaseosa",
  "sku": "COCA-350",
  "barcode": "7501055301274",
  "category": 1,
  "price": "2500.00",
  "cost": "1500.00",
  "stock": 100,
  "min_stock": 20,
  "is_active": true
}
```

#### Productos con Stock Bajo
```http
GET /api/inventory/products/low_stock/
```

### Movimientos de Inventario

#### Listar Movimientos
```http
GET /api/inventory/stock-movements/
```

#### Registrar Movimiento
```http
POST /api/inventory/stock-movements/
Content-Type: application/json

{
  "product": 1,
  "movement_type": "in",
  "quantity": 50,
  "reason": "Compra a proveedor"
}
```

Tipos de movimiento:
- `in`: Entrada
- `out`: Salida
- `adjust`: Ajuste

## Módulo de Ventas

### Ventas

#### Listar Ventas
```http
GET /api/sales/sales/
```

Parámetros:
- `status`: completed, cancelled, pending
- `payment_method`: cash, card, transfer
- `customer`: ID del cliente
- `cashier`: ID del cajero

#### Crear Venta
```http
POST /api/sales/sales/
Content-Type: application/json

{
  "customer": 1,
  "payment_method": "cash",
  "notes": "Venta regular",
  "items": [
    {
      "product": 1,
      "quantity": 2,
      "unit_price": "2500.00",
      "discount": "0.00"
    },
    {
      "product": 2,
      "quantity": 1,
      "unit_price": "5000.00",
      "discount": "500.00"
    }
  ]
}
```

#### Ventas del Día
```http
GET /api/sales/sales/today_sales/
```

**Respuesta:**
```json
{
  "date": "2024-01-15",
  "total_sales": 150000.00,
  "transaction_count": 25,
  "average_sale": 6000.00
}
```

#### Ventas por Periodo
```http
GET /api/sales/sales/sales_by_period/?period=week
```

Periodos disponibles: `day`, `week`, `month`, `year`

#### Cancelar Venta
```http
POST /api/sales/sales/{id}/cancel/
```

## Módulo de Fidelización

### Clientes

#### Listar Clientes
```http
GET /api/loyalty/customers/
```

#### Crear Cliente
```http
POST /api/loyalty/customers/
Content-Type: application/json

{
  "name": "María González",
  "email": "maria@example.com",
  "phone": "3001234567",
  "address": "Calle 123 #45-67"
}
```

#### Redimir Puntos
```http
POST /api/loyalty/customers/{id}/redeem_points/
Content-Type: application/json

{
  "points": 100,
  "description": "Descuento del 10%"
}
```

### Transacciones de Puntos

#### Listar Transacciones
```http
GET /api/loyalty/transactions/
```

Parámetros:
- `customer`: ID del cliente
- `transaction_type`: earn, redeem, adjust

### Recompensas

#### Listar Recompensas
```http
GET /api/loyalty/rewards/
```

#### Crear Recompensa
```http
POST /api/loyalty/rewards/
Content-Type: application/json

{
  "name": "Descuento 10%",
  "description": "10% de descuento en tu próxima compra",
  "points_required": 100,
  "is_active": true
}
```

## Módulo de Reportes

### Generar Reporte de Ventas
```http
POST /api/reports/reports/generate_sales_report/
Content-Type: application/json

{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
```

**Respuesta:**
```json
{
  "id": 1,
  "name": "Reporte de Ventas 2024-01-01 - 2024-01-31",
  "report_type": "sales",
  "date_from": "2024-01-01",
  "date_to": "2024-01-31",
  "data": {
    "total_sales": 500000.00,
    "transaction_count": 150,
    "average_sale": 3333.33,
    "payment_methods": [...],
    "top_products": [...]
  },
  "generated_by_name": "admin",
  "created_at": "2024-01-31T12:00:00Z"
}
```

### Generar Reporte de Inventario
```http
POST /api/reports/reports/generate_inventory_report/
Content-Type: application/json

{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
```

### Generar Reporte de Clientes
```http
POST /api/reports/reports/generate_customer_report/
Content-Type: application/json

{
  "date_from": "2024-01-01",
  "date_to": "2024-01-31"
}
```

## Paginación

Todos los endpoints de lista soportan paginación:

```http
GET /api/inventory/products/?page=2&page_size=20
```

**Respuesta:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/inventory/products/?page=3",
  "previous": "http://localhost:8000/api/inventory/products/?page=1",
  "results": [...]
}
```

## Filtros y Búsqueda

### Búsqueda
```http
GET /api/inventory/products/?search=coca
```

### Filtros
```http
GET /api/sales/sales/?status=completed&payment_method=cash
```

### Ordenamiento
```http
GET /api/inventory/products/?ordering=-created_at
```

Prefijo `-` para orden descendente.

## Códigos de Respuesta

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Eliminación exitosa
- `400 Bad Request`: Datos inválidos
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Errores

Formato de error:
```json
{
  "detail": "Mensaje de error",
  "field_name": ["Error específico del campo"]
}
```

## Rate Limiting

En producción, se recomienda implementar rate limiting:
- 100 solicitudes por minuto por usuario autenticado
- 20 solicitudes por minuto por IP no autenticada
