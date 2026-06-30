#!/bin/bash
set -e

echo "Esperando a que PostgreSQL esté listo..."
until pg_isready -h db -p 5432 -U "${POSTGRES_USER:-alimendata_user}" -d "${POSTGRES_DB:-alimendata}"; do
    sleep 2
done
echo "PostgreSQL está listo."

# 1. Ejecutar migraciones (Estructura)
echo "Ejecutando migraciones de Alembic..."
alembic upgrade head

# 2. Ingesta Automática (Datos) usando ORM en lugar de psql
echo "Verificando estado de los datos..."
DATA_EXISTS=$(python -m app.seed.check_db product_count || echo "0")

if [ -z "$DATA_EXISTS" ]; then
  DATA_EXISTS=0
fi

if [ "$DATA_EXISTS" -eq "0" ]; then
    echo "Base de datos vacía. Iniciando Pipeline de Ingestión Histórica..."
    
    echo "Generando registros (15 años)..."
    python -m app.seed.generator
    
    echo "Cargando datos a PostgreSQL via ORM..."
    python -m app.seed.loader
    
    echo "Generando visualizaciones analíticas iniciales..."
    python -m app.analytics.visualization
    
    echo "Pipeline completado exitosamente."
else
    echo "Datos detectados ($DATA_EXISTS productos). Saltando fase de ingesta."
fi

# 3. Lanzar la aplicación
echo "Iniciando AlimenData API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload