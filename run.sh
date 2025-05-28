#!/bin/bash
# Script que construye e inicia el contenedor Docker

# Nos aseguramos de estar en el directorio del script
cd "$(dirname "$0")"

# Construir e iniciar el contenedor
docker-compose up -d --build