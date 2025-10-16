# Guía de Inicio Rápido - Ecomix

Esta guía te ayudará a tener Ecomix funcionando en **5 minutos**.

## Pre-requisitos

- Python 3.8 o superior instalado
- Git instalado

## Pasos de Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/MrSony01/Ecomix---Sistema-de-ventas-para-comercio-local.git
cd Ecomix---Sistema-de-ventas-para-comercio-local
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
python manage.py migrate
```

### 5. Cargar Datos de Prueba

```bash
python manage.py load_initial_data
```

Este comando crea:
- 3 usuarios de prueba
- 5 categorías de productos
- 4 productos de ejemplo
- 3 clientes
- 4 recompensas

### 6. Iniciar el Servidor

```bash
python manage.py runserver
```

## Acceso al Sistema

### Panel de Administración
- URL: http://localhost:8000/admin/
- Usuario: `admin`
- Contraseña: `admin123`

### Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin   | admin123   | Administrador |
| cajero  | cajero123  | Cajero |
| gerente | gerente123 | Gerente |

### Frontend

Abre los archivos HTML en tu navegador:
- **Login**: `templates/login.html`
- **Dashboard**: `templates/index.html` (requiere login)
- **Punto de Venta**: `templates/pos.html` (requiere login)

**Nota**: Para que el frontend funcione correctamente, asegúrate de que el servidor Django esté corriendo en el puerto 8000.

## Uso Rápido

### 1. Login
1. Abre `templates/login.html` en tu navegador
2. Ingresa usuario: `cajero` y contraseña: `cajero123`
3. Haz clic en "Iniciar Sesión"

### 2. Realizar una Venta
1. Serás redirigido al dashboard
2. Haz clic en "Nueva Venta" o ve a `templates/pos.html`
3. Selecciona productos haciendo clic en ellos
4. Ajusta cantidades si es necesario
5. Selecciona un cliente (opcional)
6. Elige método de pago
7. Haz clic en "Completar Venta"

### 3. Ver Reportes
1. Accede al panel de administración
2. Ve a la sección de Reportes
3. O usa la API:
   ```bash
   curl -X GET http://localhost:8000/api/sales/sales/today_sales/
   ```

## API REST

### Obtener Token de Autenticación

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

### Listar Productos

```bash
curl -X GET http://localhost:8000/api/inventory/products/ \
  -H "Authorization: Bearer TU_TOKEN_ACCESS"
```

### Crear Venta

```bash
curl -X POST http://localhost:8000/api/sales/sales/ \
  -H "Authorization: Bearer TU_TOKEN_ACCESS" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "cash",
    "items": [
      {
        "product": 1,
        "quantity": 2,
        "unit_price": "2500.00",
        "discount": "0.00"
      }
    ]
  }'
```

## Estructura del Proyecto

```
ecomix/
├── ecomix_backend/      # Configuración Django
├── users/               # Gestión de usuarios
├── inventory/           # Inventario
├── sales/               # Ventas (POS)
├── loyalty/             # Fidelización
├── reports/             # Reportes
├── templates/           # Frontend HTML
├── static/              # CSS y JavaScript
├── manage.py
└── requirements.txt
```

## Comandos Útiles

```bash
# Crear superusuario adicional
python manage.py createsuperuser

# Ver estructura de la base de datos
python manage.py dbshell

# Ejecutar tests
python manage.py test

# Verificar proyecto
python manage.py check

# Limpiar base de datos y recargar datos
rm db.sqlite3
python manage.py migrate
python manage.py load_initial_data
```

## Problemas Comunes

### Error: "No module named 'django'"
```bash
pip install django
```

### Error: "Port 8000 already in use"
```bash
# Usa otro puerto
python manage.py runserver 8001
```

### Frontend no conecta con API
1. Verifica que el servidor Django esté corriendo
2. Verifica que la URL en `static/js/api.js` sea correcta
3. Abre la consola del navegador para ver errores

## Próximos Pasos

1. ✅ Explora el panel de administración
2. ✅ Prueba el punto de venta
3. ✅ Revisa la documentación de la API
4. ✅ Lee la documentación completa en `README.md`
5. ✅ Consulta `DOCUMENTATION.md` para detalles técnicos

## Soporte

- 📚 Documentación completa: Ver `README.md`
- 🔧 API: Ver `API.md`
- 🚀 Despliegue: Ver `DEPLOYMENT.md`
- 🤝 Contribuir: Ver `CONTRIBUTING.md`

## Licencia

MIT License - Ver `LICENSE` para más detalles.

---

**¡Disfruta usando Ecomix!** 🎉

Si encuentras útil este proyecto, considera darle una ⭐ en GitHub.
