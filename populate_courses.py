#!/usr/bin/env python3
"""
Script para poblar la tabla de cursos de DynamoDB con al menos 2000 cursos
y generar un archivo CSV con los cursos insertados.

Uso:
    python populate_courses.py

Requisitos:
    - AWS CLI configurado con credenciales válidas
    - Permisos de escritura en la tabla de DynamoDB
    - Python 3.7+
    - Dependencias: boto3, botocore
"""

import boto3
import csv
import json
import os
import random
import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Dict
import time
from config import (
    AWS_REGION, TABLE_NAME, TENANT_ID, TOTAL_COURSES, 
    BATCH_SIZE, DELAY_BETWEEN_BATCHES, CSV_OUTPUT_DIR
)

# Crear directorio de salida si no existe
os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)
CSV_FILENAME = os.path.join(CSV_OUTPUT_DIR, f'cursos_insertados_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')

class CourseGenerator:
    def __init__(self):
        # Datos de ejemplo para generar cursos realistas
        self.course_names = [
            "Introducción a Python", "JavaScript Avanzado", "React desde Cero", "Node.js Completo",
            "Machine Learning Básico", "Data Science con Python", "AWS Cloud Practitioner",
            "Docker y Kubernetes", "Desarrollo Web Full Stack", "Angular Fundamentals",
            "Vue.js Masterclass", "TypeScript Esencial", "MongoDB Avanzado", "PostgreSQL Completo",
            "Cybersecurity Fundamentals", "Ethical Hacking", "DevOps con Jenkins", "Git y GitHub",
            "Algoritmos y Estructuras de Datos", "Programación Orientada a Objetos",
            "Microservicios con Spring Boot", "Flutter Development", "React Native",
            "Unity Game Development", "Blender 3D Modeling", "Photoshop CC",
            "Digital Marketing", "SEO Optimization", "Google Analytics", "Social Media Marketing",
            "Excel Avanzado", "Power BI", "Tableau", "SQL para Principiantes",
            "Java Spring Framework", "C# .NET Core", "PHP Laravel", "Ruby on Rails",
            "Golang Programming", "Rust Programming", "Swift iOS Development", "Kotlin Android",
            "Blockchain Development", "Cryptocurrency Trading", "NFT Creation", "Web3 Development",
            "UI/UX Design", "Figma Masterclass", "Adobe XD", "Sketch Design",
            "Project Management", "Agile Scrum", "Leadership Skills", "Communication Skills"
        ]
        
        self.instructors = [
            "Dr. María González", "Prof. Carlos Rodríguez", "Ing. Ana Martínez", "Lic. Pedro López",
            "Dra. Laura Fernández", "Ing. Miguel Torres", "Prof. Carmen Ruiz", "Dr. José García",
            "Lic. Isabel Moreno", "Ing. Roberto Jiménez", "Dra. Patricia Herrera", "Prof. Antonio Silva",
            "Ing. Lucía Vargas", "Dr. Fernando Castro", "Lic. Mónica Ortega", "Prof. Diego Ramírez",
            "Dra. Cristina Mendoza", "Ing. Alejandro Peña", "Lic. Beatriz Aguilar", "Prof. Raúl Vega"
        ]
        
        self.categories = [
            ["Programación", "Python"], ["Programación", "JavaScript"], ["Desarrollo Web", "Frontend"],
            ["Desarrollo Web", "Backend"], ["Desarrollo Web", "Full Stack"], ["Ciencia de Datos", "Machine Learning"],
            ["Ciencia de Datos", "Analytics"], ["Cloud Computing", "AWS"], ["Cloud Computing", "Azure"],
            ["DevOps", "Docker"], ["DevOps", "Kubernetes"], ["Bases de Datos", "SQL"],
            ["Bases de Datos", "NoSQL"], ["Seguridad", "Cybersecurity"], ["Seguridad", "Ethical Hacking"],
            ["Móvil", "Android"], ["Móvil", "iOS"], ["Móvil", "React Native"], ["Móvil", "Flutter"],
            ["Diseño", "UI/UX"], ["Diseño", "Gráfico"], ["Marketing", "Digital"], ["Marketing", "SEO"],
            ["Negocios", "Management"], ["Negocios", "Leadership"], ["Blockchain", "Cryptocurrency"],
            ["Blockchain", "Web3"], ["Juegos", "Unity"], ["Juegos", "Unreal Engine"]
        ]
        
        self.levels = ["Principiante", "Intermedio", "Avanzado", "Experto"]
        
        self.durations = [
            "2 horas", "4 horas", "6 horas", "8 horas", "10 horas", "12 horas",
            "15 horas", "20 horas", "25 horas", "30 horas", "40 horas", "50 horas"
        ]

    def generate_course(self) -> Dict:
        """Genera un curso con datos aleatorios pero realistas"""
        base_name = random.choice(self.course_names)
        variation = random.choice(["Completo", "Avanzado", "Desde Cero", "Masterclass", "Práctico", "2024"])
        nombre = f"{base_name} - {variation}"
        
        # Generar descripción
        descripcion = f"Aprende {base_name.lower()} de manera práctica y efectiva. " \
                     f"Este curso te llevará desde los conceptos básicos hasta técnicas avanzadas. " \
                     f"Incluye proyectos reales y ejercicios prácticos para consolidar tu aprendizaje."
        
        # Precios realistas - usar Decimal para DynamoDB
        precio_original = random.randint(50, 200)
        precio = random.randint(20, precio_original)
        
        course = {
            'tenant_id': TENANT_ID,
            'curso_id': str(uuid.uuid4()),
            'nombre': nombre,
            'descripcion': descripcion,
            'instructor': random.choice(self.instructors),
            'precio': Decimal(str(precio)),
            'rating': Decimal(str(round(random.uniform(3.5, 5.0), 1))),
            'estudiantes': str(random.randint(100, 50000)),
            'duracion': random.choice(self.durations),
            'imagen_url': f"https://example.com/images/curso_{uuid.uuid4().hex[:8]}.jpg",
            'categories': random.choice(self.categories),
            'nivel': random.choice(self.levels)
        }
        
        return course

def setup_dynamodb():
    """Configura el cliente de DynamoDB"""
    try:
        dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        table = dynamodb.Table(TABLE_NAME)
        
        # Verificar que la tabla existe
        table.load()
        print(f"✅ Conectado a la tabla: {TABLE_NAME}")
        return table
    except Exception as e:
        print(f"❌ Error conectando a DynamoDB: {e}")
        return None

def batch_write_courses(table, courses: List[Dict]) -> bool:
    """Escribe un lote de cursos a DynamoDB"""
    try:
        with table.batch_writer() as batch:
            for course in courses:
                batch.put_item(Item=course)
        return True
    except Exception as e:
        print(f"❌ Error escribiendo lote: {e}")
        return False

def write_to_csv(courses: List[Dict], filename: str):
    """Escribe los cursos a un archivo CSV"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'tenant_id', 'curso_id', 'nombre', 'descripcion', 'instructor',
                'precio', 'precio_original', 'rating', 'estudiantes', 'duracion',
                'imagen_url', 'categories', 'nivel'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for course in courses:
                # Convertir Decimal a float para CSV y categorías a string
                course_copy = course.copy()
                course_copy['precio'] = float(course['precio'])
                course_copy['rating'] = float(course['rating'])
                course_copy['categories'] = json.dumps(course['categories'])
                writer.writerow(course_copy)
        
        print(f"✅ CSV generado: {filename}")
    except Exception as e:
        print(f"❌ Error generando CSV: {e}")

def main():
    """Función principal"""
    print("🚀 Iniciando población de cursos...")
    print(f"📊 Objetivo: {TOTAL_COURSES} cursos")
    print(f"🏢 Tenant ID: {TENANT_ID}")
    print(f"📋 Tabla: {TABLE_NAME}")
    print("-" * 50)
    
    # Configurar DynamoDB
    table = setup_dynamodb()
    if not table:
        return
    
    # Generar cursos
    generator = CourseGenerator()
    all_courses = []
    successful_inserts = 0
    failed_inserts = 0
    
    print("📝 Generando y insertando cursos...")
    
    for i in range(0, TOTAL_COURSES, BATCH_SIZE):
        batch_courses = []
        batch_end = min(i + BATCH_SIZE, TOTAL_COURSES)
        
        # Generar lote de cursos
        for j in range(i, batch_end):
            course = generator.generate_course()
            batch_courses.append(course)
        
        # Insertar lote en DynamoDB
        if batch_write_courses(table, batch_courses):
            successful_inserts += len(batch_courses)
            all_courses.extend(batch_courses)
            print(f"✅ Lote {i//BATCH_SIZE + 1}: {len(batch_courses)} cursos insertados "
                  f"(Total: {successful_inserts}/{TOTAL_COURSES})")
        else:
            failed_inserts += len(batch_courses)
            print(f"❌ Lote {i//BATCH_SIZE + 1}: Error insertando {len(batch_courses)} cursos")
        
        # Pequeña pausa para evitar throttling
        time.sleep(DELAY_BETWEEN_BATCHES)
    
    print("-" * 50)
    print(f"📊 Resumen de inserción:")
    print(f"   ✅ Exitosos: {successful_inserts}")
    print(f"   ❌ Fallidos: {failed_inserts}")
    print(f"   📈 Tasa de éxito: {(successful_inserts/TOTAL_COURSES)*100:.1f}%")
    
    # Generar CSV
    if all_courses:
        print(f"\n📄 Generando archivo CSV...")
        write_to_csv(all_courses, CSV_FILENAME)
        print(f"✅ Archivo CSV generado: {CSV_FILENAME}")
    
    print("\n🎉 Proceso completado!")

if __name__ == "__main__":
    main()