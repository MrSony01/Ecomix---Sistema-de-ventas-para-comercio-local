# Guía de Despliegue en Producción - Ecomix

Esta guía te ayudará a desplegar Ecomix en un entorno de producción.

## Requisitos Previos

- Servidor Linux (Ubuntu 20.04 LTS o superior recomendado)
- Python 3.8+
- PostgreSQL 12+
- Nginx
- Certificado SSL (Let's Encrypt recomendado)
- Dominio configurado

## 1. Preparar el Servidor

### Actualizar sistema
```bash
sudo apt update
sudo apt upgrade -y
```

### Instalar dependencias
```bash
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx git
```

## 2. Configurar PostgreSQL

### Crear base de datos y usuario
```bash
sudo -u postgres psql

CREATE DATABASE ecomix_db;
CREATE USER ecomix_user WITH PASSWORD 'tu_contraseña_segura';
ALTER ROLE ecomix_user SET client_encoding TO 'utf8';
ALTER ROLE ecomix_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecomix_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecomix_db TO ecomix_user;
\q
```

## 3. Configurar la Aplicación

### Clonar repositorio
```bash
cd /var/www
sudo git clone https://github.com/MrSony01/Ecomix---Sistema-de-ventas-para-comercio-local.git ecomix
cd ecomix
```

### Crear entorno virtual
```bash
sudo python3 -m venv venv
sudo chown -R $USER:$USER venv
source venv/bin/activate
```

### Instalar dependencias
```bash
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Configurar variables de entorno
```bash
sudo nano .env
```

Agregar:
```env
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

DATABASE_URL=postgresql://ecomix_user:tu_contraseña_segura@localhost:5432/ecomix_db

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# CORS
CORS_ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
```

### Actualizar settings.py para producción
```python
# ecomix_backend/settings.py
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='ecomix_db'),
        'USER': config('DB_USER', default='ecomix_user'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

### Ejecutar migraciones
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py load_initial_data
python manage.py createsuperuser
```

## 4. Configurar Gunicorn

### Crear archivo de configuración
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Agregar:
```ini
[Unit]
Description=Gunicorn daemon for Ecomix
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/ecomix
Environment="PATH=/var/www/ecomix/venv/bin"
ExecStart=/var/www/ecomix/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/ecomix/ecomix.sock \
          ecomix_backend.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Iniciar Gunicorn
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

## 5. Configurar Nginx

### Crear configuración del sitio
```bash
sudo nano /etc/nginx/sites-available/ecomix
```

Agregar:
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/ecomix/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/ecomix/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/ecomix/ecomix.sock;
    }
}
```

### Habilitar sitio
```bash
sudo ln -s /etc/nginx/sites-available/ecomix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. Configurar SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

La configuración de Nginx se actualizará automáticamente para HTTPS.

## 7. Configurar Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

## 8. Mantenimiento

### Actualizar la aplicación
```bash
cd /var/www/ecomix
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Ver logs
```bash
# Gunicorn logs
sudo journalctl -u gunicorn

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Django logs
tail -f /var/www/ecomix/logs/django.log
```

### Backup de base de datos
```bash
# Crear backup
sudo -u postgres pg_dump ecomix_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
sudo -u postgres psql ecomix_db < backup_20240101.sql
```

## 9. Optimizaciones

### Redis para Caché (Opcional)
```bash
sudo apt install redis-server
pip install django-redis
```

Agregar a settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Configurar workers de Gunicorn
Ajusta el número de workers según tu servidor:
```
workers = (2 x CPU_cores) + 1
```

## 10. Monitoreo

### Configurar logs de Django
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/www/ecomix/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## 11. Seguridad Adicional

### Fail2Ban para protección contra fuerza bruta
```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Actualizar sistema regularmente
```bash
sudo apt update && sudo apt upgrade -y
```

### Configurar backups automáticos
Crear script de backup:
```bash
#!/bin/bash
# /usr/local/bin/backup_ecomix.sh

BACKUP_DIR="/backups/ecomix"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup de base de datos
sudo -u postgres pg_dump ecomix_db > $BACKUP_DIR/db_$DATE.sql

# Backup de media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/ecomix/media

# Limpiar backups antiguos (mayores a 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete
```

Agregar a crontab:
```bash
sudo crontab -e
# Agregar línea:
0 2 * * * /usr/local/bin/backup_ecomix.sh
```

## Solución de Problemas

### Error 502 Bad Gateway
```bash
# Verificar que Gunicorn esté corriendo
sudo systemctl status gunicorn
sudo systemctl restart gunicorn

# Verificar permisos del socket
ls -l /var/www/ecomix/ecomix.sock
```

### Error de permisos en archivos estáticos
```bash
sudo chown -R www-data:www-data /var/www/ecomix
sudo chmod -R 755 /var/www/ecomix
```

### Base de datos no conecta
```bash
# Verificar PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -c "SELECT version();"
```

## Recursos Adicionales

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

## Soporte

Para problemas de despliegue, abrir un issue en GitHub con:
- Sistema operativo y versión
- Logs relevantes
- Pasos para reproducir el problema
