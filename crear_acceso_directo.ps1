# ========================================
# Crear Acceso Directo en Escritorio
# ========================================

Write-Host "`n╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Creando acceso directo en el escritorio...     ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Rutas
$projectPath = $PSScriptRoot
$batFile = Join-Path $projectPath "Iniciar_App.bat"
$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Intelligent Document Finder.lnk"

# Verificar que existe el .bat
if (-not (Test-Path $batFile)) {
    Write-Host "[ERROR] No se encontró Iniciar_App.bat" -ForegroundColor Red
    pause
    exit 1
}

# Crear objeto de acceso directo
$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $batFile
$Shortcut.WorkingDirectory = $projectPath
$Shortcut.Description = "Intelligent Document Finder v1.3.0 - Búsqueda de documentos con IA"
$Shortcut.WindowStyle = 1  # Normal window

# Intentar usar icono si existe
$iconPath = Join-Path $projectPath "src\ui\icons\app.ico"
if (Test-Path $iconPath) {
    $Shortcut.IconLocation = $iconPath
}

# Guardar acceso directo
$Shortcut.Save()

Write-Host "✅ Acceso directo creado exitosamente!" -ForegroundColor Green
Write-Host "📍 Ubicación: $shortcutPath" -ForegroundColor White
Write-Host "`n💡 Ahora puedes hacer doble clic en el icono del escritorio para abrir la app.`n" -ForegroundColor Yellow

pause
