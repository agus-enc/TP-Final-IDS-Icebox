#!/bin/bash
set -e
echo "--- INICIANDO BACKEND ---"
echo "Esperando a que MySQL esté listo..."
sleep 15
echo "Corriendo seeder si hace falta..."
python seeder.py
echo "Levantando servidor Flask..."
exec flask run --host=0.0.0.0 --port=5000