#!/usr/bin/env python3
"""
Script para verificar que los cursos se insertaron correctamente en DynamoDB
"""

import boto3
from config import AWS_REGION, TABLE_NAME, TENANT_ID

def verify_courses():
    """Verifica la inserción de cursos en DynamoDB"""
    try:
        # Configurar DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table(TABLE_NAME)
        
        print(f"🔍 Verificando cursos en tabla: {TABLE_NAME}")
        print(f"🏢 Tenant ID: {TENANT_ID}")
        print("-" * 50)
        
        # Contar total de elementos en la tabla
        response = table.scan(Select='COUNT')
        total_items = response['Count']
        print(f"📊 Total de elementos en la tabla: {total_items}")
        
        # Contar elementos para el tenant específico
        response = table.query(
            KeyConditionExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': TENANT_ID},
            Select='COUNT'
        )
        tenant_items = response['Count']
        print(f"🏢 Elementos para tenant '{TENANT_ID}': {tenant_items}")
        
        # Obtener algunos ejemplos
        response = table.query(
            KeyConditionExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': TENANT_ID},
            Limit=3
        )
        
        print(f"\n📋 Ejemplos de cursos insertados:")
        print("-" * 50)
        
        for i, item in enumerate(response['Items'], 1):
            print(f"\n{i}. {item['nombre']}")
            print(f"   Instructor: {item['instructor']}")
            print(f"   Precio: ${item['precio']} (Original: ${item.get('precio_original', 'N/A')})")
            print(f"   Rating: {item.get('rating', 'N/A')}/5.0")
            print(f"   Nivel: {item.get('nivel', 'N/A')}")
            print(f"   Categorías: {item.get('categories', [])}")
            print(f"   Duración: {item.get('duracion', 'N/A')}")
        
        # Verificar distribución por categorías
        print(f"\n📈 Análisis de categorías:")
        print("-" * 50)
        
        response = table.query(
            KeyConditionExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': TENANT_ID}
        )
        
        category_count = {}
        level_count = {}
        
        for item in response['Items']:
            # Contar categorías
            categories = item.get('categories', [])
            if categories and len(categories) > 0:
                main_category = categories[0]
                category_count[main_category] = category_count.get(main_category, 0) + 1
            
            # Contar niveles
            level = item.get('nivel', 'Sin nivel')
            level_count[level] = level_count.get(level, 0) + 1
        
        print("Distribución por categoría principal:")
        for category, count in sorted(category_count.items()):
            print(f"  {category}: {count} cursos")
        
        print("\nDistribución por nivel:")
        for level, count in sorted(level_count.items()):
            print(f"  {level}: {count} cursos")
        
        print(f"\n✅ Verificación completada!")
        
        if tenant_items >= 2000:
            print(f"🎉 ¡Éxito! Se insertaron {tenant_items} cursos (objetivo: 2000+)")
        else:
            print(f"⚠️  Solo se encontraron {tenant_items} cursos (objetivo: 2000+)")
            
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")

if __name__ == "__main__":
    verify_courses()