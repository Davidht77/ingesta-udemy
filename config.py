"""
Configuración para el script de población de cursos
"""

# Configuración de AWS
AWS_REGION = 'us-east-1'
TABLE_NAME = 'dev_cursos'  # Cambia según tu stage (dev_cursos, prod_cursos, etc.)

# Configuración del tenant
# Puedes obtener este valor de tu base de datos de usuarios o usar uno por defecto
TENANT_ID = 'UDEMY'

# Configuración del script
TOTAL_COURSES = 1000  # Número total de cursos a generar
BATCH_SIZE = 20       # Tamaño del lote para escritura en DynamoDB
DELAY_BETWEEN_BATCHES = 0.1  # Segundos de espera entre lotes para evitar throttling

# Configuración de archivos
CSV_OUTPUT_DIR = './output'  # Directorio donde se guardará el CSV