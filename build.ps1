param(
  [string]$Mode = "folder",
  [switch]$Clean,
  [switch]$Sign,
  [string]$CertPath = $null,
  [string]$TimestampUrl = "http://timestamp.sectigo.com"
)

Write-Host "🚀 INTELLIGENT DOCUMENT FINDER - BUILD OPTIMIZADO" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green

# Crear/activar entorno virtual si no existe
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
  Write-Host "==> Creando entorno..." -ForegroundColor Cyan
  python -m venv .venv
}
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

Write-Host "==> Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt

Write-Host "==> Pre-cargando modelo (opcional)..." -ForegroundColor Cyan
python scripts/preload_model.py
if ($LASTEXITCODE -ne 0) {
  Write-Host "    Nota: El modelo se descargará en el primer uso de la aplicación." -ForegroundColor Yellow
}

if ($Clean) {
  Write-Host "🧹 Limpiando builds previos..." -ForegroundColor Yellow
  Remove-Item -Recurse -Force build, dist, __pycache__ -ErrorAction SilentlyContinue
}

Write-Host "🔨 Construyendo ejecutable (Modo: $Mode)..." -ForegroundColor Cyan
Write-Host "    Por favor NO interrumpas el proceso aunque parezca detenido." -ForegroundColor Yellow

if ($Mode -eq "folder") {
  Write-Host "📁 Usando spec optimizado (idf_optimized.spec)..." -ForegroundColor Gray
  pyinstaller --noconfirm idf_optimized.spec
} elseif ($Mode -eq "onefile") {
  Write-Host "📄 Usando spec onefile (idf_onefile.spec)..." -ForegroundColor Gray
  pyinstaller --noconfirm idf_onefile.spec
} else {
  Write-Host "❌ Modo desconocido: $Mode (usa 'folder' o 'onefile')" -ForegroundColor Red
  exit 1
}

if ($Sign) {
  Write-Host "🔏 Firmando ejecutables..." -ForegroundColor Cyan
  $signtool = (Get-Command signtool -ErrorAction SilentlyContinue)
  if (-not $signtool) {
    Write-Host "⚠ No se encontró 'signtool' en PATH. Omite la firma o instala Windows SDK." -ForegroundColor Yellow
  } else {
    $files = @()
    if ($Mode -eq 'folder') { $files = Get-ChildItem -Recurse -Filter *.exe dist\IntelligentDocumentFinder }
    if ($Mode -eq 'onefile') { $files = Get-ChildItem dist -Filter *.exe }
    foreach ($f in $files) {
      if ($CertPath) {
        & $signtool sign /f $CertPath /fd SHA256 /tr $TimestampUrl /td SHA256 $f.FullName
      } else {
        Write-Host "⚠ Sin certificado especificado (-CertPath). Saltando firma de $($f.Name)." -ForegroundColor Yellow
      }
    }
  }
}

Write-Host "==> Listo. Revisa /dist" -ForegroundColor Green
