# Guía de Instalación - Ecomix

## Requisitos del Sistema

### Software Requerido
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### Opcional
- PostgreSQL 12+ (para producción)
- Redis (para caché en producción)
- Nginx (para servir archivos estáticos en producción)

## Instalación Paso a Paso

### 1. Preparar el Entorno

#### Windows
```bash
# Verificar instalación de Python
python --version

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate
```

#### Linux/Mac
```bash
# Verificar instalación de Python
python3 --version

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

#### Desarrollo (SQLite)
```bash
# Crear las migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

#### Producción (PostgreSQL)
```bash
# Instalar adaptador PostgreSQL
pip install psycopg2-binary

# Actualizar settings.py con configuración de PostgreSQL
# Ver sección de Configuración de Base de Datos más abajo
```

### 4. Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear:
- Nombre de usuario
- Correo electrónico
- Contraseña

### 5. Cargar Datos de Prueba (Opcional)

```bash
# Si existen fixtures
python manage.py loaddata initial_data.json
```

### 6. Ejecutar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://localhost:8000`

### 7. Acceder al Sistema

- **Panel de Administración**: `http://localhost:8000/admin/`
- **Frontend**: `http://localhost:8000/` (abrir templates/login.html en navegador)

## Configuración Avanzada

### Base de Datos PostgreSQL

Editar `ecomix_backend/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ecomix_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://user:password@localhost:5432/ecomix_db

# Producción
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Archivos Estáticos (Producción)

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput
```

## Verificación de Instalación

### 1. Verificar Servidor
```bash
curl http://localhost:8000/api/
```

### 2. Verificar API
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_contraseña"}'
```

### 3. Verificar Frontend
Abrir en navegador: `templates/login.html`

## Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
```

### Error: "Migration already exists"
```bash
# Eliminar migraciones y base de datos
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
rm db.sqlite3

# Recrear migraciones
python manage.py makemigrations
python manage.py migrate
```

### Error: "Port already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Error: "CORS issues"
Verificar `CORS_ALLOWED_ORIGINS` en `settings.py`

## Siguientes Pasos

1. Acceder al panel de administración
2. Crear categorías de productos
3. Agregar productos al inventario
4. Crear clientes
5. Probar el punto de venta
6. Generar reportes

## Soporte

Para problemas de instalación, abrir un issue en GitHub con:
- Sistema operativo
- Versión de Python
- Mensaje de error completo
- Pasos para reproducir el problema
