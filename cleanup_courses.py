#!/usr/bin/env python3
"""
Script para limpiar/eliminar cursos de la tabla DynamoDB
¡USAR CON PRECAUCIÓN! Este script elimina datos permanentemente.
"""

import boto3
from config import AWS_REGION, TABLE_NAME, TENANT_ID

def cleanup_courses():
    """Elimina todos los cursos del tenant especificado"""
    
    # Confirmación de seguridad
    print("⚠️  ADVERTENCIA: Este script eliminará TODOS los cursos del tenant especificado.")
    print(f"🏢 Tenant ID: {TENANT_ID}")
    print(f"📋 Tabla: {TABLE_NAME}")
    print(f"🌍 Región: {AWS_REGION}")
    
    confirmation = input("\n¿Estás seguro de que quieres continuar? (escribe 'ELIMINAR' para confirmar): ")
    
    if confirmation != 'ELIMINAR':
        print("❌ Operación cancelada.")
        return
    
    try:
        # Configurar DynamoDB
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table(TABLE_NAME)
        
        print(f"\n🔍 Buscando cursos para eliminar...")
        
        # Obtener todos los cursos del tenant
        response = table.query(
            KeyConditionExpression='tenant_id = :tenant_id',
            ExpressionAttributeValues={':tenant_id': TENANT_ID}
        )
        
        items_to_delete = response['Items']
        total_items = len(items_to_delete)
        
        if total_items == 0:
            print("ℹ️  No se encontraron cursos para eliminar.")
            return
        
        print(f"📊 Se encontraron {total_items} cursos para eliminar.")
        
        final_confirmation = input(f"\n¿Confirmas la eliminación de {total_items} cursos? (escribe 'SÍ' para confirmar): ")
        
        if final_confirmation != 'SI':
            print("❌ Operación cancelada.")
            return
        
        print(f"\n🗑️  Eliminando cursos...")
        
        # Eliminar en lotes
        deleted_count = 0
        batch_size = 25
        
        with table.batch_writer() as batch:
            for item in items_to_delete:
                batch.delete_item(
                    Key={
                        'tenant_id': item['tenant_id'],
                        'curso_id': item['curso_id']
                    }
                )
                deleted_count += 1
                
                if deleted_count % batch_size == 0:
                    print(f"   Eliminados: {deleted_count}/{total_items}")
        
        print(f"\n✅ Eliminación completada!")
        print(f"🗑️  Total eliminados: {deleted_count} cursos")
        
    except Exception as e:
        print(f"❌ Error durante la eliminación: {e}")

if __name__ == "__main__":
    cleanup_courses()