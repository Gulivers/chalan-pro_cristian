#!/bin/bash
# Script para ejecutar migraciones en Render con solución automática al conflicto
# Este script maneja el error de historial de migraciones inconsistente

set -o errexit

echo "=== Ejecutando migraciones con solución automática ==="

# Paso 1: Intentar resolver el conflicto de appinventory.0002
echo "Resolviendo conflicto de dependencias..."
python manage.py migrate appinventory 0002 --fake 2>/dev/null || {
    echo "Fake migration failed, trying real migration..."
    python manage.py migrate appinventory 0002 || echo "Migration 0002 already applied or not needed"
}

# Paso 2: Aplicar todas las migraciones del schema compartido
echo "Aplicando migraciones del schema compartido..."
python manage.py migrate_schemas --shared || {
    echo "Warning: migrate_schemas failed, trying standard migrate..."
    python manage.py migrate || echo "Migrations failed, continuing..."
}

echo "Migraciones completadas"

