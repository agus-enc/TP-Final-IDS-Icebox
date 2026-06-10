#!/bin/bash

# Salir inmediatamente si algún comando falla
set -e

echo "--- INICIANDO CONFIGURACIÓN AUTOMÁTICA DE ICEBOX ---"

echo "🧹 Limpiando procesos previos..."
pkill -f "flask" || true
pkill -f "python3 -m flask" || true

#Libera los puertos que usamos
fuser -k 5000/tcp 2>/dev/null || true   
fuser -k 8000/tcp 2>/dev/null || true

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual de Python (venv)..."
    python3 -m venv venv
else
    echo "✔ El entorno virtual (venv) ya existe."
fi

echo "🔄 Activando el entorno virtual..."
source venv/bin/activate

echo "Actualizando pip e instalando dependencias desde requirements.txt..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "❌ Error crítico: No se encontró el archivo requirements.txt en la raíz."
    exit 1
fi

echo "🗄️ Configurando MySQL..."
if [ -d "backend" ]; then
    
    cd backend
    
    echo "Creando base de datos y tablas desde init.sql..."
    python3 init_db.py
    
    echo "Poblando tablas con países y ciudades desde JSON (seeder.py)..."
    python3 seeder.py
    
    cd ..
else
    echo "❌ Error crítico: No se encontró la carpeta /backend."
    exit 1
fi

echo "Levantando el servidor BACKEND en el puerto 5000..."
export FLASK_APP=backend/app.py
export FLASK_DEBUG=1
export PYTHONPATH="$PWD/backend/endpoints"

python3 backend/app.py &

echo "⏳ Esperando a que el Backend esté completamente activo..."

# Bucle: comprueba si el puerto 5000 ya está escuchando conexiones
while ! nc -z localhost 5000; do   
  sleep 2
done

echo "¡Backend detectado y respondiendo en el puerto 5000!"

echo "Levantando el servidor FRONTEND en el puerto 8000..."
export FLASK_APP=frontend/app.py
export FLASK_DEBUG=1
python3 frontend/app.py