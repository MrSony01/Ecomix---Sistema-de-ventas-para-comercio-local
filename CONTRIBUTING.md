# Guía de Contribución - Ecomix

¡Gracias por tu interés en contribuir a Ecomix! Esta guía te ayudará a comenzar.

## Código de Conducta

- Sé respetuoso con otros colaboradores
- Acepta críticas constructivas
- Enfócate en lo que es mejor para la comunidad
- Muestra empatía hacia otros miembros de la comunidad

## ¿Cómo Contribuir?

### Reportar Bugs

1. Verifica que el bug no haya sido reportado anteriormente
2. Abre un nuevo issue con:
   - Descripción clara del problema
   - Pasos para reproducir el bug
   - Comportamiento esperado vs. actual
   - Screenshots si es aplicable
   - Información del entorno (OS, Python version, etc.)

### Sugerir Mejoras

1. Abre un issue describiendo la mejora
2. Explica por qué sería útil
3. Proporciona ejemplos de uso si es posible

### Pull Requests

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/MrSony01/Ecomix---Sistema-de-ventas-para-comercio-local.git
   ```

2. **Crea una rama para tu feature**
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```

3. **Realiza tus cambios**
   - Sigue el estilo de código del proyecto
   - Añade tests para nuevas funcionalidades
   - Actualiza la documentación si es necesario

4. **Ejecuta los tests**
   ```bash
   python manage.py test
   ```

5. **Commit tus cambios**
   ```bash
   git commit -m "feat: descripción clara de los cambios"
   ```

6. **Push a tu fork**
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

7. **Abre un Pull Request**
   - Describe tus cambios claramente
   - Referencia cualquier issue relacionado

## Estándares de Código

### Python (Backend)

- Sigue PEP 8
- Usa nombres descriptivos para variables y funciones
- Documenta funciones complejas
- Máximo 80-100 caracteres por línea

Ejemplo:
```python
def calculate_total_with_discount(subtotal, discount_percentage):
    """
    Calculate the total amount after applying discount.
    
    Args:
        subtotal (Decimal): The subtotal amount
        discount_percentage (int): Discount percentage (0-100)
    
    Returns:
        Decimal: Total amount after discount
    """
    discount_amount = subtotal * (discount_percentage / 100)
    return subtotal - discount_amount
```

### JavaScript (Frontend)

- Usa ES6+ features
- Usa nombres descriptivos
- Comenta código complejo
- Usa async/await para operaciones asíncronas

Ejemplo:
```javascript
async function fetchProducts() {
    try {
        const response = await apiRequest('/inventory/products/');
        return response.results;
    } catch (error) {
        console.error('Error fetching products:', error);
        throw error;
    }
}
```

### HTML/CSS

- Usa indentación consistente (2 o 4 espacios)
- Usa nombres de clase descriptivos
- Sigue la estructura de Bootstrap

## Tests

- Escribe tests para nuevas funcionalidades
- Asegúrate de que todos los tests pasen antes de hacer un PR
- Apunta a una cobertura de código del 80% o más

```bash
# Ejecutar todos los tests
python manage.py test

# Ejecutar tests de una app específica
python manage.py test users

# Con cobertura
coverage run --source='.' manage.py test
coverage report
```

## Estructura de Commits

Usa commits semánticos:

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan código)
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Cambios en build, dependencias, etc.

Ejemplos:
```
feat: add customer loyalty tier calculation
fix: resolve stock update issue in POS
docs: update API documentation for sales endpoint
```

## Proceso de Revisión

1. Tu PR será revisado por un mantenedor
2. Puede que se soliciten cambios
3. Una vez aprobado, será merged a la rama principal
4. Tu contribución será reconocida en el README

## Configuración del Entorno de Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/MrSony01/Ecomix---Sistema-de-ventas-para-comercio-local.git
cd Ecomix---Sistema-de-ventas-para-comercio-local

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py load_initial_data

# Ejecutar servidor
python manage.py runserver
```

## Áreas de Contribución

### Backend
- Optimización de consultas a la base de datos
- Mejoras en la API
- Nuevos endpoints
- Mejoras en seguridad

### Frontend
- Mejoras en la UI/UX
- Nuevas páginas
- Optimización de JavaScript
- Responsividad

### Testing
- Aumentar cobertura de tests
- Tests de integración
- Tests end-to-end

### Documentación
- Mejorar README
- Documentar API
- Tutoriales
- Traducciones

## Contacto

Si tienes preguntas, puedes:
- Abrir un issue de discusión
- Contactar a los mantenedores

## Licencia

Al contribuir, aceptas que tus contribuciones se licenciarán bajo la misma licencia del proyecto.

¡Gracias por contribuir a Ecomix! 🎉
