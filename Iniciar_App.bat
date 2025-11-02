@echo off
REM ========================================
REM Intelligent Document Finder - Launcher
REM ========================================

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║   Intelligent Document Finder v1.3.0            ║
echo ║   Iniciando aplicacion...                       ║
echo ╚══════════════════════════════════════════════════╝
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Verificar si existe Python en el entorno virtual
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual.
    echo Por favor ejecuta: python -m venv .venv
    pause
    exit /b 1
)

REM Ejecutar app directamente con el Python del entorno virtual
.venv\Scripts\python.exe src/app.py

REM Si la app cierra con error, mantener ventana abierta
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion termino con errores.
    pause
)
