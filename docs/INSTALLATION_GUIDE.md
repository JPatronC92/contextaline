# 🚀 Guía de Instalación Completa

## Índice
1. [Instalación Rápida](#instalación-rápida)
2. [Instalación desde Ejecutable](#instalación-desde-ejecutable-windows)
3. [Instalación desde Código](#instalación-desde-código-fuente)
4. [Configuración de Desarrollo](#configuración-de-desarrollo)
5. [Solución de Problemas](#solución-de-problemas)

---

## Instalación Rápida

### Windows - Método más fácil

```powershell
# 1. Clonar repositorio
git clone https://github.com/JPatronC92/contextaline.git
cd contextaline

# 2. Ejecutar demo (instala dependencias automáticamente)
.\demo.ps1

# 3. Crear acceso directo en escritorio
.\crear_acceso_directo.ps1
```

Después, simplemente haz doble clic en el icono del escritorio.

---

## Instalación desde Ejecutable (Windows)

### Opción 1: Instalador MSI

1. Descarga `DocumentIntelligence_Setup_1.3.0.exe` desde [Releases](https://github.com/JPatronC92/contextaline/releases)
2. Ejecuta el instalador
3. Sigue el asistente de instalación
4. Lanza desde el menú de inicio: `Intelligent Document Finder`

**Ventajas:**
- ✅ No requiere Python instalado
- ✅ Instalación guiada
- ✅ Acceso directo automático
- ✅ Desinstalación desde Panel de Control

### Opción 2: Ejecutable Portable

1. Descarga `IntelligentDocumentFinder_v1.3.0.zip`
2. Extrae en cualquier carpeta
3. Ejecuta `IntelligentDocumentFinder.exe`

**Ventajas:**
- ✅ No requiere instalación
- ✅ Portable (USB, nube)
- ✅ No modifica el sistema

---

## Instalación desde Código Fuente

### Requisitos Previos

- **Python**: 3.8 o superior ([Descargar](https://www.python.org/downloads/))
- **Git**: Para clonar el repositorio ([Descargar](https://git-scm.com/))
- **Espacio**: 500MB libres
- **RAM**: Mínimo 4GB (8GB recomendado)

### Paso 1: Clonar Repositorio

```bash
# HTTPS
git clone https://github.com/JPatronC92/contextaline.git

# SSH (si tienes configurada)
git clone git@github.com:JPatronC92/contextaline.git

# Entrar al directorio
cd contextaline
```

### Paso 2: Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
# Crear entorno virtual
python -m venv .venv

# Activar
.\.venv\Scripts\Activate.ps1

# Si hay error de permisos:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
# Upgrade pip primero
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### Paso 4: Ejecutar Aplicación

**Método 1: Python directo**
```bash
python src/app.py
```

**Método 2: Launcher (Windows)**
```powershell
# Doble clic en:
Iniciar_App.bat
```

**Método 3: Acceso directo (Windows)**
```powershell
# Crear acceso directo en escritorio
.\crear_acceso_directo.ps1

# Luego usar el icono del escritorio
```

---

## Configuración de Desarrollo

### Setup IDE

#### Visual Studio Code

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

#### PyCharm

1. `File > Settings > Project > Python Interpreter`
2. Click ⚙️ > `Add...`
3. Select `Existing environment`
4. Browse to `.venv/Scripts/python.exe`

### Instalar Dependencias de Desarrollo

```bash
# Herramientas de desarrollo
pip install black pylint pytest pytest-cov

# Pre-commit hooks (opcional)
pip install pre-commit
pre-commit install
```

### Ejecutar Tests

```bash
# Test básico
python tests/smoke_test.py

# Con pytest (si instalado)
pytest tests/

# Con coverage
pytest --cov=src tests/
```

---

## Dependencias Detalladas

### Obligatorias

```txt
PyQt6>=6.4.0              # Framework GUI
pypdf>=3.0.0              # Lectura de PDFs
python-docx>=0.8.11       # Lectura de Word
numpy>=1.21.0             # Operaciones numéricas
scikit-learn>=1.0.0       # TF-IDF (fallback)
```

### Opcionales (IA Completa)

```txt
torch>=2.0.0              # PyTorch para IA
sentence-transformers     # Modelos Sentence-BERT
transformers>=4.0.0       # Transformers de Hugging Face
```

**Nota:** Si no instalas las dependencias opcionales, la app usa modo TF-IDF (75% precisión vs 92% con IA).

### Instalar Solo IA

```bash
# Solo componentes de IA
pip install torch sentence-transformers transformers
```

### Instalar Sin IA (más ligero)

```bash
# Crear requirements_basic.txt
PyQt6>=6.4.0
pypdf>=3.0.0
python-docx>=0.8.11
numpy>=1.21.0
scikit-learn>=1.0.0

# Instalar
pip install -r requirements_basic.txt
```

---

## Compilar Ejecutable

### Windows

```powershell
# Método 1: Script automatizado
.\build.ps1

# Método 2: PyInstaller manual
pip install pyinstaller
pyinstaller idf_optimized.spec

# Output: dist/IntelligentDocumentFinder/
```

### Linux/macOS

```bash
# Dar permisos
chmod +x build.sh

# Compilar
./build.sh

# Output: dist/IntelligentDocumentFinder/
```

### Crear Instalador (Windows)

Requiere [Inno Setup](https://jrsoftware.org/isinfo.php):

```powershell
# Compilar primero
.\build.ps1

# Crear instalador
iscc scripts\installer.iss

# Output: dist/installer/DocumentIntelligence_Setup_1.3.0.exe
```

---

## Solución de Problemas

### Error: "python no se reconoce"

**Problema:** Python no está en PATH.

**Solución Windows:**
1. Reinstalar Python con "Add to PATH" marcado
2. O añadir manualmente: `C:\Users\<User>\AppData\Local\Programs\Python\Python3X`

**Solución Linux/macOS:**
```bash
# Usar python3 en lugar de python
python3 -m venv .venv
```

### Error: "pip install falla"

**Problema:** pip desactualizado o problemas de red.

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Usar cache si hay problemas de red
pip install --cache-dir ./pip-cache -r requirements.txt

# Instalar uno por uno si falla
pip install PyQt6
pip install pypdf
# etc...
```

### Error: "No module named 'PyQt6'"

**Problema:** Entorno virtual no activado o dependencias no instaladas.

**Solución:**
```bash
# Verificar entorno virtual activado
# El prompt debe mostrar (.venv)

# Si no:
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Torch not available"

**Problema:** PyTorch no instalado (esto es normal).

**Solución:** La app funciona en modo TF-IDF. Para IA completa:
```bash
pip install torch sentence-transformers
```

### Error al ejecutar desde .bat

**Problema:** Ruta incorrecta o entorno virtual en otra ubicación.

**Solución:** Editar `Iniciar_App.bat`:
```batch
REM Cambiar esta línea si .venv está en otro lugar
.venv\Scripts\python.exe src/app.py
```

### App se cierra inmediatamente

**Problema:** Error de Python no visible.

**Solución:** Ejecutar desde terminal para ver errores:
```bash
python src/app.py
```

### Búsqueda muy lenta

**Solución:**
1. Primera búsqueda siempre es lenta (crea caché)
2. Evitar carpetas con >10,000 archivos
3. Cerrar otros programas pesados
4. Aumentar RAM disponible

---

## Actualizar a Nueva Versión

### Desde Código

```bash
# 1. Pull cambios
git pull origin main

# 2. Actualizar dependencias
pip install --upgrade -r requirements.txt

# 3. Ejecutar
python src/app.py
```

### Desde Ejecutable

1. Descargar nueva versión desde Releases
2. Desinstalar versión anterior (opcional)
3. Instalar nueva versión
4. Licencia se mantiene automáticamente

---

## Desinstalación

### Desde Ejecutable
- Windows: Panel de Control > Programas > Desinstalar

### Desde Código
```bash
# Eliminar carpeta del proyecto
cd ..
rm -rf contextaline  # Linux/Mac
Remove-Item -Recurse -Force contextaline  # Windows PowerShell
```

### Limpiar Datos de Usuario

**Windows:**
```powershell
Remove-Item -Recurse -Force "$env:APPDATA\JulioDevs\IDF"
```

**Linux/macOS:**
```bash
rm -rf ~/.cache/idf
```

---

## Recursos Adicionales

- 📖 [README Principal](../README.md)
- 📝 [Changelog](../CHANGELOG.md)
- ❓ [FAQ](../FAQ.md)
- 🏗️ [Build Instructions](BUILD_INSTRUCTIONS.md)
- 🤝 [Contributing](../CONTRIBUTING.md)
- 🔒 [Security](../SECURITY.md)

---

## Soporte

¿Problemas con la instalación?

- 🐛 [Reportar Issue](https://github.com/JPatronC92/contextaline/issues)
- 💬 [Discussions](https://github.com/JPatronC92/contextaline/discussions)
- 📧 Email: soporte@juliodevs.com

---

**¡Listo para empezar!** 🚀

Una vez instalado, consulta la [Guía de Presentación](PRESENTATION_GUIDE.md) o las [Notas Rápidas](DEMO_QUICK_NOTES.md) para aprender a usar todas las funciones.
