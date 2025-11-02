@echo off
REM ========================================
REM Limpiar Caché y Ejecutar App
REM ========================================

echo.
echo ╔══════════════════════════════════════════════════╗
echo ║   Intelligent Document Finder v1.3.0            ║
echo ║   Limpiando cache y ejecutando...              ║
echo ╚══════════════════════════════════════════════════╝
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0"

REM Paso 1: Eliminar archivos de cache
echo [1/4] Eliminando archivos __pycache__...
if exist "src\__pycache__" (
    rmdir /s /q "src\__pycache__" 2>nul
    echo     ✓ src\__pycache__ eliminado
)
if exist "__pycache__" (
    rmdir /s /q "__pycache__" 2>nul
    echo     ✓ __pycache__ eliminado
)

REM Paso 2: Eliminar archivos .pyc
echo [2/4] Eliminando archivos .pyc...
del /s /q "*.pyc" >nul 2>&1
echo     ✓ Archivos .pyc eliminados

REM Paso 3: Verificar entorno virtual
echo [3/4] Verificando entorno virtual...
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] No se encontro el entorno virtual.
    echo Por favor ejecuta: python -m venv .venv
    pause
    exit /b 1
)
echo     ✓ Entorno virtual encontrado

REM Paso 4: Ejecutar app directamente
echo [4/4] Ejecutando aplicacion actualizada...
echo.
.venv\Scripts\python.exe src/app.py

REM Si la app cierra con error, mantener ventana abierta
if errorlevel 1 (
    echo.
    echo [ERROR] La aplicacion termino con errores.
    pause
)
