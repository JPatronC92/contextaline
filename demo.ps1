# 🎬 Script de Demo - IntelligentDocumentFinder v1.3.0
# Ejecuta este script para iniciar la demo automáticamente

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🔍 IntelligentDocumentFinder v1.3.0  " -ForegroundColor Yellow
Write-Host "     Demo Preparation Script           " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verificar entorno virtual
Write-Host "📦 Verificando entorno virtual..." -ForegroundColor Green
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "   ✓ Entorno virtual encontrado" -ForegroundColor Green
} else {
    Write-Host "   ✗ Entorno virtual no encontrado. Creándolo..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "   ✓ Entorno virtual creado" -ForegroundColor Green
}

# 2. Activar entorno virtual
Write-Host ""
Write-Host "🔧 Activando entorno virtual..." -ForegroundColor Green
& .venv\Scripts\Activate.ps1

# 3. Verificar dependencias
Write-Host ""
Write-Host "📚 Verificando dependencias..." -ForegroundColor Green
$pipList = pip list 2>$null
if ($pipList -match "PyQt6") {
    Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "   ! Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt --quiet
    Write-Host "   ✓ Dependencias instaladas" -ForegroundColor Green
}

# 4. Verificar documentos de prueba
Write-Host ""
Write-Host "📄 Verificando documentos de prueba..." -ForegroundColor Green
if (Test-Path "test_documents") {
    $fileCount = (Get-ChildItem -Path "test_documents" -File).Count
    Write-Host "   ✓ $fileCount documentos de prueba disponibles" -ForegroundColor Green
} else {
    Write-Host "   ! Carpeta de prueba no encontrada" -ForegroundColor Yellow
}

# 5. Mostrar información de demo
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎯 Información para la Demo          " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 LICENCIAS DE PRUEBA:" -ForegroundColor Magenta
Write-Host "   JDL-8FK6-IRLY-A5R1" -ForegroundColor White
Write-Host "   JDL-0LSF-ZDPJ-ULQB" -ForegroundColor White
Write-Host "   JDL-83B1-8WXZ-J416" -ForegroundColor White
Write-Host ""
Write-Host "🔍 BÚSQUEDAS DE EJEMPLO:" -ForegroundColor Magenta
Write-Host "   • contratos de servicios 2024" -ForegroundColor White
Write-Host "   • documentos técnicos y manuales" -ForegroundColor White
Write-Host "   • informes y reportes importantes" -ForegroundColor White
Write-Host ""
Write-Host "⌨️  ATAJOS DE TECLADO A MOSTRAR:" -ForegroundColor Magenta
Write-Host "   Ctrl+O  - Abrir carpeta" -ForegroundColor White
Write-Host "   Ctrl+F  - Enfocar búsqueda" -ForegroundColor White
Write-Host "   Enter   - Ejecutar búsqueda" -ForegroundColor White
Write-Host "   F1      - Ayuda completa" -ForegroundColor White
Write-Host ""
Write-Host "🎨 CARACTERÍSTICAS A DESTACAR:" -ForegroundColor Magenta
Write-Host "   ✓ Búsqueda inteligente con IA" -ForegroundColor White
Write-Host "   ✓ Resultados con colores (🟢🟡🟠)" -ForegroundColor White
Write-Host "   ✓ Menú contextual (clic derecho)" -ForegroundColor White
Write-Host "   ✓ Historial de búsquedas" -ForegroundColor White
Write-Host "   ✓ Metadata detallada" -ForegroundColor White
Write-Host ""

# 6. Countdown para iniciar
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Iniciando aplicación en:" -ForegroundColor Yellow
for ($i = 3; $i -gt 0; $i--) {
    Write-Host "   $i..." -ForegroundColor Yellow
    Start-Sleep -Seconds 1
}

Write-Host ""
Write-Host "✨ ¡Lanzando IntelligentDocumentFinder!" -ForegroundColor Green
Write-Host ""

# 7. Lanzar aplicación
python src/app.py

# 8. Mensaje post-cierre
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Demo finalizada - ¡Gracias! 👋       " -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
