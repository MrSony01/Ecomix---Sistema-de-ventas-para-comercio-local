# Documentación del Proyecto - Ecomix

## Índice

1. [Visión General](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Modelos de Datos](#modelos-de-datos)
4. [Metodología](#metodología)
5. [Calidad del Software](#calidad-del-software)
6. [Seguridad](#seguridad)
7. [Casos de Uso](#casos-de-uso)

## Visión General

Ecomix es un sistema web completo de ventas diseñado específicamente para comercios locales. Combina un potente backend construido con Django REST Framework y un frontend moderno con Bootstrap 5 para ofrecer una solución integral de gestión empresarial.

### Objetivo del Proyecto

Proporcionar a los comercios locales una herramienta eficiente, segura y fácil de usar para:
- Gestionar su inventario
- Procesar ventas rápidamente
- Fidelizar clientes
- Tomar decisiones basadas en datos

### Alcance

- **Backend**: API REST completa con Django
- **Frontend**: Interfaz responsive con Bootstrap
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación**: JWT (JSON Web Tokens)
- **Seguridad**: Implementación de estándares OWASP

## Arquitectura

### Arquitectura General

```
┌─────────────────┐
│   Frontend      │
│  (Bootstrap +   │
│   JavaScript)   │
└────────┬────────┘
         │ HTTP/HTTPS
         │ REST API
┌────────▼────────┐
│   Backend       │
│   (Django +     │
│    DRF)         │
└────────┬────────┘
         │
┌────────▼────────┐
│   Database      │
│ (SQLite/       │
│  PostgreSQL)    │
└─────────────────┘
```

### Capas de la Aplicación

1. **Capa de Presentación** (Frontend)
   - Templates HTML
   - CSS con Bootstrap
   - JavaScript para interactividad
   - Comunicación con API REST

2. **Capa de Aplicación** (Backend)
   - Django Views y ViewSets
   - Serializers
   - Autenticación JWT
   - Lógica de negocio

3. **Capa de Datos**
   - Modelos Django ORM
   - Migraciones
   - Base de datos relacional

## Modelos de Datos

### Diagrama Entidad-Relación

```
┌─────────────┐       ┌──────────────┐
│    User     │       │   Category   │
├─────────────┤       ├──────────────┤
│ - username  │       │ - name       │
│ - email     │       │ - description│
│ - role      │       └──────┬───────┘
│ - phone     │              │
└──────┬──────┘              │
       │                     │
       │                     │
┌──────▼──────┐       ┌──────▼───────┐
│    Sale     │       │   Product    │
├─────────────┤       ├──────────────┤
│ - number    │       │ - name       │
│ - total     │       │ - sku        │
│ - payment   │◄──────┤ - price      │
│ - status    │       │ - stock      │
└──────┬──────┘       └──────┬───────┘
       │                     │
       │                     │
┌──────▼──────┐       ┌──────▼───────┐
│  Customer   │       │ SaleItem     │
├─────────────┤       ├──────────────┤
│ - name      │       │ - quantity   │
│ - phone     │       │ - unit_price │
│ - points    │       │ - total      │
└─────────────┘       └──────────────┘
```

### Descripción de Modelos

#### User (users)
- **Propósito**: Gestión de usuarios del sistema
- **Roles**: Admin, Gerente, Cajero
- **Campos clave**: username, email, role, phone

#### Category (inventory)
- **Propósito**: Organizar productos
- **Campos clave**: name, description

#### Product (inventory)
- **Propósito**: Gestión de productos
- **Campos clave**: name, sku, barcode, price, cost, stock

#### Sale (sales)
- **Propósito**: Registrar transacciones de venta
- **Campos clave**: sale_number, total, payment_method, status

#### SaleItem (sales)
- **Propósito**: Detalles de productos en una venta
- **Campos clave**: product, quantity, unit_price, total

#### Customer (loyalty)
- **Propósito**: Gestión de clientes y fidelización
- **Campos clave**: name, phone, loyalty_points, total_purchases

#### LoyaltyTransaction (loyalty)
- **Propósito**: Historial de puntos de fidelidad
- **Campos clave**: customer, points, transaction_type

## Metodología

### Scrum

El proyecto fue desarrollado siguiendo la metodología Scrum:

#### Roles
- **Product Owner**: Define requisitos y prioridades
- **Scrum Master**: Facilita el proceso
- **Equipo de Desarrollo**: Implementa funcionalidades

#### Ceremonias
- **Sprint Planning**: Planificación de sprints de 2 semanas
- **Daily Scrum**: Reuniones diarias de 15 minutos
- **Sprint Review**: Demostración de funcionalidades
- **Sprint Retrospective**: Mejora continua

#### Artefactos
- **Product Backlog**: Lista priorizada de funcionalidades
- **Sprint Backlog**: Tareas del sprint actual
- **Incremento**: Producto funcional al final de cada sprint

### Sprints Realizados

**Sprint 1**: Configuración inicial y modelos
- Setup del proyecto Django
- Creación de modelos de datos
- Configuración de base de datos

**Sprint 2**: API REST y autenticación
- Implementación de serializers
- Creación de endpoints
- Sistema de autenticación JWT

**Sprint 3**: Frontend y punto de venta
- Diseño de interfaces
- Implementación de POS
- Integración con API

**Sprint 4**: Testing y documentación
- Escritura de tests
- Documentación de API
- Guías de usuario

## Calidad del Software

### ISO 25010

El proyecto cumple con los siguientes aspectos de calidad según ISO 25010:

#### 1. Funcionalidad
- ✅ Completitud funcional
- ✅ Corrección funcional
- ✅ Pertinencia funcional

#### 2. Eficiencia de Desempeño
- ✅ Comportamiento temporal (respuestas rápidas)
- ✅ Utilización de recursos
- ✅ Capacidad

#### 3. Compatibilidad
- ✅ Coexistencia
- ✅ Interoperabilidad (API REST)

#### 4. Usabilidad
- ✅ Reconocibilidad de la adecuación
- ✅ Capacidad de aprendizaje
- ✅ Operabilidad
- ✅ Protección contra errores de usuario
- ✅ Estética de la interfaz

#### 5. Fiabilidad
- ✅ Madurez
- ✅ Disponibilidad
- ✅ Tolerancia a fallos
- ✅ Capacidad de recuperación

#### 6. Seguridad
- ✅ Confidencialidad (JWT, encriptación)
- ✅ Integridad (validaciones)
- ✅ No repudio
- ✅ Responsabilidad
- ✅ Autenticidad

#### 7. Mantenibilidad
- ✅ Modularidad
- ✅ Reusabilidad
- ✅ Analizabilidad
- ✅ Capacidad de ser modificado
- ✅ Capacidad de ser probado

#### 8. Portabilidad
- ✅ Adaptabilidad
- ✅ Capacidad de instalación
- ✅ Capacidad de ser reemplazado

## Seguridad

### Implementación OWASP Top 10

#### A01:2021 - Broken Access Control
- ✅ Control de acceso basado en roles
- ✅ Validación de permisos en cada endpoint
- ✅ Autenticación requerida

#### A02:2021 - Cryptographic Failures
- ✅ HTTPS en producción
- ✅ Contraseñas hasheadas
- ✅ Tokens JWT seguros

#### A03:2021 - Injection
- ✅ ORM de Django previene SQL injection
- ✅ Validación de entrada
- ✅ Sanitización de datos

#### A04:2021 - Insecure Design
- ✅ Diseño con seguridad en mente
- ✅ Límites de tasa implementables
- ✅ Validación de lógica de negocio

#### A05:2021 - Security Misconfiguration
- ✅ DEBUG=False en producción
- ✅ Headers de seguridad configurados
- ✅ Secretos en variables de entorno

#### A06:2021 - Vulnerable Components
- ✅ Dependencias actualizadas
- ✅ Versiones estables de librerías

#### A07:2021 - Identification and Authentication
- ✅ JWT para autenticación
- ✅ Políticas de contraseñas fuertes
- ✅ Sesiones seguras

#### A08:2021 - Software and Data Integrity
- ✅ Validaciones de integridad
- ✅ Control de versiones

#### A09:2021 - Security Logging
- ✅ Logging configurado
- ✅ Auditoría de acciones

#### A10:2021 - Server-Side Request Forgery
- ✅ Validación de URLs
- ✅ CSRF protection

## Casos de Uso

### CU-01: Realizar Venta
**Actor**: Cajero
**Precondición**: Usuario autenticado, productos en inventario
**Flujo**:
1. Cajero busca productos
2. Agrega productos al carrito
3. Selecciona cliente (opcional)
4. Confirma método de pago
5. Completa la venta
**Postcondición**: Venta registrada, inventario actualizado, puntos acumulados

### CU-02: Gestionar Inventario
**Actor**: Administrador/Gerente
**Precondición**: Usuario autenticado con permisos
**Flujo**:
1. Accede al módulo de inventario
2. Crea/edita productos
3. Registra movimientos de stock
4. Consulta productos con stock bajo
**Postcondición**: Inventario actualizado

### CU-03: Consultar Reportes
**Actor**: Gerente/Administrador
**Precondición**: Usuario autenticado
**Flujo**:
1. Accede al módulo de reportes
2. Selecciona tipo de reporte
3. Define rango de fechas
4. Genera reporte
**Postcondición**: Reporte generado y visualizado

### CU-04: Gestionar Clientes
**Actor**: Cajero/Gerente
**Precondición**: Usuario autenticado
**Flujo**:
1. Accede al módulo de clientes
2. Registra nuevo cliente
3. Consulta puntos de fidelidad
4. Redime puntos
**Postcondición**: Cliente registrado/actualizado

## Conclusiones

Ecomix es un sistema completo y robusto que cumple con:
- ✅ Requisitos funcionales del comercio local
- ✅ Estándares de calidad ISO 25010
- ✅ Mejores prácticas de seguridad OWASP
- ✅ Metodología ágil Scrum
- ✅ Arquitectura escalable y mantenible

El sistema está preparado para evolucionar y adaptarse a las necesidades cambiantes del negocio.
