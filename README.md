# Script de Población de Cursos para DynamoDB

Este script pobla la tabla de cursos de DynamoDB con al menos 2,000 cursos realistas y genera un archivo CSV con todos los cursos insertados.

## Características

- ✅ Genera 2,000+ cursos con datos realistas
- ✅ Inserción por lotes para mejor rendimiento
- ✅ Manejo de errores y reintentos
- ✅ Generación automática de CSV
- ✅ Configuración personalizable
- ✅ Progreso en tiempo real

## Requisitos Previos

1. **AWS CLI configurado** con credenciales válidas
2. **Permisos de DynamoDB** para escribir en la tabla de cursos
3. **Python 3.7+**
4. **Dependencias de Python** (ver requirements.txt)

## Instalación

1. Clona o descarga los archivos del script
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración

Edita el archivo `config.py` para ajustar la configuración:

```python
# Configuración de AWS
AWS_REGION = 'us-east-1'
TABLE_NAME = 'dev_cursos'  # Cambia según tu stage
TENANT_ID = 'default_tenant'  # Tu tenant ID

# Configuración del script
TOTAL_COURSES = 2000  # Número de cursos a generar
BATCH_SIZE = 25       # Tamaño del lote
```

### Parámetros Importantes

- **TABLE_NAME**: Nombre de tu tabla DynamoDB (ej: `dev_cursos`, `prod_cursos`)
- **TENANT_ID**: ID del tenant para el cual crear los cursos
- **TOTAL_COURSES**: Número total de cursos a generar (mínimo 2000)
- **AWS_REGION**: Región de AWS donde está tu tabla

## Uso

### Ejecución Básica

```bash
python populate_courses.py
```

### Verificar Configuración AWS

Antes de ejecutar, verifica que tienes acceso a AWS:

```bash
aws sts get-caller-identity
aws dynamodb describe-table --table-name dev_cursos
```

## Estructura de Datos

Cada curso generado incluye:

```json
{
  "tenant_id": "default_tenant",
  "curso_id": "uuid-generado",
  "nombre": "Nombre del Curso - Variación",
  "descripcion": "Descripción detallada del curso",
  "instructor": "Nombre del Instructor",
  "precio": 45,
  "precio_original": 120,
  "rating": 4.5,
  "estudiantes": "15000",
  "duracion": "20 horas",
  "imagen_url": "https://example.com/images/curso_abc123.jpg",
  "categories": ["Programación", "Python"],
  "nivel": "Intermedio"
}
```

## Salida

El script genera:

1. **Inserción en DynamoDB**: Cursos insertados directamente en la tabla
2. **Archivo CSV**: `output/cursos_insertados_YYYYMMDD_HHMMSS.csv`
3. **Reporte de progreso**: Estadísticas en tiempo real

### Ejemplo de Salida

```
🚀 Iniciando población de cursos...
📊 Objetivo: 2000 cursos
🏢 Tenant ID: default_tenant
📋 Tabla: dev_cursos
--------------------------------------------------
✅ Conectado a la tabla: dev_cursos
📝 Generando y insertando cursos...
✅ Lote 1: 25 cursos insertados (Total: 25/2000)
✅ Lote 2: 25 cursos insertados (Total: 50/2000)
...
--------------------------------------------------
📊 Resumen de inserción:
   ✅ Exitosos: 2000
   ❌ Fallidos: 0
   📈 Tasa de éxito: 100.0%

📄 Generando archivo CSV...
✅ CSV generado: output/cursos_insertados_20240715_143022.csv

🎉 Proceso completado!
```

## Solución de Problemas

### Error de Credenciales AWS

```
❌ Error conectando a DynamoDB: Unable to locate credentials
```

**Solución**: Configura AWS CLI o variables de entorno:
```bash
aws configure
# o
export AWS_ACCESS_KEY_ID=tu_access_key
export AWS_SECRET_ACCESS_KEY=tu_secret_key
export AWS_SESSION_TOKEN=tu_session_token  # Si usas AWS Academy
```

### Error de Tabla No Encontrada

```
❌ Error conectando a DynamoDB: Requested resource not found
```

**Solución**: Verifica que:
1. El nombre de la tabla en `config.py` sea correcto
2. La tabla exista en la región especificada
3. Tengas permisos para acceder a la tabla

### Throttling de DynamoDB

Si ves errores de throttling, ajusta en `config.py`:
```python
BATCH_SIZE = 10  # Reduce el tamaño del lote
DELAY_BETWEEN_BATCHES = 0.5  # Aumenta el delay
```

## Personalización

### Agregar Más Categorías

Edita la lista `categories` en la clase `CourseGenerator`:

```python
self.categories = [
    ["Tu Categoría", "Subcategoría"],
    # ... más categorías
]
```

### Cambiar Datos de Cursos

Modifica las listas en `CourseGenerator.__init__()`:
- `course_names`: Nombres base de cursos
- `instructors`: Lista de instructores
- `levels`: Niveles de dificultad
- `durations`: Duraciones disponibles

## Archivos del Proyecto

- `populate_courses.py`: Script principal
- `config.py`: Configuración del script
- `requirements.txt`: Dependencias de Python
- `README.md`: Este archivo de documentación

## Notas Importantes

- El script usa `batch_writer` de boto3 para optimizar las escrituras
- Los UUIDs se generan automáticamente para cada curso
- Los precios y ratings son realistas pero aleatorios
- Las imágenes usan URLs de ejemplo (deberás reemplazarlas con URLs reales)
- El script respeta los límites de DynamoDB para evitar throttling

## Verificación Post-Ejecución

Para verificar que los cursos se insertaron correctamente:

```bash
# Contar elementos en la tabla
aws dynamodb scan --table-name dev_cursos --select "COUNT"

# Ver algunos elementos
aws dynamodb scan --table-name dev_cursos --limit 5
```

O usa el endpoint de tu API:
```bash
curl -H "Authorization: Bearer tu_token" \
     https://tu-api-gateway-url/cursos?limit=10
```