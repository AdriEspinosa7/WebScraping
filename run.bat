@echo off
REM Script para ejecutar el scraper con Docker Compose en Windows

cd /d %~dp0
docker-compose up --build
pause