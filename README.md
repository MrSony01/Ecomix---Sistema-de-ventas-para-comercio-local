# Ecomix - Sistema de Ventas para Comercio Local

Sistema web completo de ventas para comercio local con gestión de inventario, punto de venta rápido, sistema de fidelización y reportes. Desarrollado con Django REST Framework + Bootstrap 5. Incluye roles de usuario, reportes automatizados y arquitectura escalable.

## 🚀 Características Principales

### Backend (Django REST API)
- **Autenticación y Autorización**: Sistema de usuarios con roles (Admin, Cajero, Gerente) usando JWT
- **Gestión de Inventario**: CRUD completo de productos, categorías y control de stock
- **Punto de Venta (POS)**: Sistema rápido de ventas con múltiples métodos de pago
- **Sistema de Fidelización**: Programa de puntos para clientes con niveles (Básico, Bronce, Plata, Oro)
- **Reportes**: Generación automática de reportes de ventas, inventario y clientes
- **API RESTful**: Endpoints completos para todas las funcionalidades

### Frontend (Bootstrap + JavaScript)
- **Dashboard Interactivo**: Métricas en tiempo real de ventas y estadísticas
- **Interfaz Responsive**: Diseño adaptable a dispositivos móviles y tablets
- **POS Intuitivo**: Interfaz de venta rápida y fácil de usar
- **Gestión Completa**: Módulos para inventario, clientes y reportes

## 📋 Requisitos

- Python 3.8+
- Django 4.2.7
- SQLite (desarrollo) / PostgreSQL (producción recomendado)

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/MrSony01/Ecomix---Sistema-de-ventas-para-comercio-local.git
cd Ecomix---Sistema-de-ventas-para-comercio-local
```

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar migraciones
```bash
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Estructura del Proyecto

```
ecomix/
├── ecomix_backend/       # Configuración del proyecto
├── users/                # Gestión de usuarios y autenticación
├── inventory/            # Módulo de inventario
├── sales/                # Módulo de ventas (POS)
├── loyalty/              # Sistema de fidelización
├── reports/              # Generación de reportes
├── templates/            # Plantillas HTML
├── static/               # Archivos estáticos (CSS, JS)
├── media/                # Archivos subidos por usuarios
└── manage.py
```

## 🔑 API Endpoints

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/refresh/` - Refrescar token

### Usuarios
- `GET /api/users/` - Listar usuarios
- `POST /api/users/` - Crear usuario
- `GET /api/users/{id}/` - Obtener usuario
- `PUT /api/users/{id}/` - Actualizar usuario
- `DELETE /api/users/{id}/` - Eliminar usuario
- `GET /api/users/me/` - Obtener usuario actual

### Inventario
- `GET /api/inventory/categories/` - Listar categorías
- `POST /api/inventory/categories/` - Crear categoría
- `GET /api/inventory/products/` - Listar productos
- `POST /api/inventory/products/` - Crear producto
- `GET /api/inventory/products/low_stock/` - Productos con stock bajo
- `GET /api/inventory/stock-movements/` - Movimientos de inventario
- `POST /api/inventory/stock-movements/` - Registrar movimiento

### Ventas
- `GET /api/sales/sales/` - Listar ventas
- `POST /api/sales/sales/` - Crear venta
- `GET /api/sales/sales/today_sales/` - Ventas del día
- `GET /api/sales/sales/sales_by_period/` - Ventas por periodo
- `POST /api/sales/sales/{id}/cancel/` - Cancelar venta

### Clientes y Fidelización
- `GET /api/loyalty/customers/` - Listar clientes
- `POST /api/loyalty/customers/` - Crear cliente
- `POST /api/loyalty/customers/{id}/redeem_points/` - Redimir puntos
- `GET /api/loyalty/transactions/` - Transacciones de puntos
- `GET /api/loyalty/rewards/` - Recompensas disponibles

### Reportes
- `GET /api/reports/reports/` - Listar reportes
- `POST /api/reports/reports/generate_sales_report/` - Generar reporte de ventas
- `POST /api/reports/reports/generate_inventory_report/` - Generar reporte de inventario
- `POST /api/reports/reports/generate_customer_report/` - Generar reporte de clientes

## 🎯 Metodología y Calidad

### Metodología Scrum
- Desarrollo iterativo e incremental
- Sprints de 2 semanas
- Reuniones diarias (Daily Scrum)
- Revisión y retrospectiva al final de cada sprint

### Calidad (ISO 25010)
- **Funcionalidad**: Cumple todos los requisitos especificados
- **Usabilidad**: Interfaz intuitiva y fácil de usar
- **Rendimiento**: Respuesta rápida en operaciones críticas
- **Mantenibilidad**: Código limpio y bien documentado
- **Seguridad**: Implementación de mejores prácticas OWASP

### Seguridad (OWASP)
- Autenticación con JWT
- Protección CSRF
- Validación de entrada
- Sanitización de datos
- Headers de seguridad configurados
- Protección contra XSS
- Gestión segura de contraseñas

## 👥 Roles de Usuario

### Administrador
- Acceso completo al sistema
- Gestión de usuarios
- Configuración del sistema
- Acceso a todos los reportes

### Gerente
- Visualización de reportes
- Gestión de inventario
- Supervisión de ventas
- Gestión de clientes

### Cajero
- Punto de venta (POS)
- Registro de ventas
- Consulta de productos
- Registro de clientes

## 🔒 Seguridad

El sistema implementa las siguientes medidas de seguridad siguiendo las directrices OWASP:

1. **Autenticación segura** con tokens JWT
2. **Protección CSRF** en formularios
3. **Encriptación de contraseñas** con algoritmos seguros
4. **Validación de entrada** en todos los endpoints
5. **Headers de seguridad** configurados (XSS, Content-Type, etc.)
6. **HTTPS** recomendado en producción
7. **Control de acceso** basado en roles

## 📊 Sistema de Fidelización

### Niveles de Membresía
- **Básico**: Clientes nuevos (< $100 en compras)
- **Bronce**: $100 - $499 en compras
- **Plata**: $500 - $999 en compras
- **Oro**: $1000+ en compras

### Acumulación de Puntos
- 1 punto por cada $10 en compras
- Los puntos pueden redimirse por descuentos o recompensas

## 🛠️ Tecnologías Utilizadas

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- Simple JWT
- Django CORS Headers
- Django Filter

### Frontend
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Vanilla JavaScript (ES6+)

### Base de Datos
- SQLite (desarrollo)
- Compatible con PostgreSQL, MySQL (producción)

## 📝 Licencia

Este proyecto es un proyecto académico para Ingeniería de Software.

## 👨‍💻 Autor

MrSony01

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.

## 📧 Contacto

Para preguntas o soporte, por favor abre un issue en el repositorio de GitHub.
