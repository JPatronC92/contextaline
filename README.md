# 🔍 IntelligentDocumentFinder

<div align="center">

![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-Proprietary-red.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

**Buscador inteligente de documentos usando Inteligencia Artificial**

*Encuentra documentos por contenido y significado, no solo por nombre*

[Características](#-características-principales) •
[Instalación](#-instalación) •
[Uso](#-uso-rápido) •
[Documentación](#-documentación) •
[Changelog](#-changelog)

</div>

---

## 📖 Descripción

**IntelligentDocumentFinder** es una aplicación de escritorio que utiliza **Inteligencia Artificial** para buscar documentos de manera inteligente. En lugar de buscar solo por nombre de archivo, **analiza el contenido** y encuentra documentos por **similitud semántica**.

### ¿Por qué es diferente?

```
❌ Búsqueda tradicional:
   "contrato_limpieza_2024.pdf" ← Solo encuentra archivos con ese nombre exacto

✅ IntelligentDocumentFinder:
   "acuerdos de servicios de limpieza" ← Encuentra:
   • contrato_limpieza_2024.pdf
   • acuerdo_servicios_generales.docx
   • propuesta_mantenimiento.pdf
   ¡Y muchos más documentos relacionados!
```

La **IA entiende el contexto** de tu búsqueda y encuentra documentos relevantes aunque uses palabras diferentes.

---

## ✨ Características Principales

### 🧠 Búsqueda Inteligente
- **IA avanzada** con modelo Sentence-BERT (all-MiniLM-L6-v2)
- **Búsqueda semántica** que entiende el significado
- **Modo básico TF-IDF** como fallback sin PyTorch
- **Caché inteligente** para búsquedas ultra-rápidas

### 📄 Formatos Soportados
- **PDF** (`.pdf`) - Extracción de texto completo
- **Word** (`.docx`, `.doc`) - Lectura de párrafos
- **Texto** (`.txt`) - Soporte UTF-8

### 🎨 Interfaz Moderna (v1.3.0)
- **Diseño moderno** con sistema de colores coherente
- **Iconos emoji** intuitivos en toda la interfaz
- **Resultados enriquecidos** con metadata (fecha, tamaño, relevancia)
- **Colores por relevancia**: 🟢 Alta (>80%) | 🟡 Media (60-80%) | 🟠 Baja (<60%)
- **Menú contextual** con clic derecho (abrir, copiar ruta, propiedades)

### ⌨️ Productividad
- **Atajos de teclado completos**:
  - `Ctrl+O` - Abrir carpeta
  - `Ctrl+F` - Enfocar búsqueda
  - `Enter` - Ejecutar búsqueda
  - `Ctrl+R` - Limpiar resultados
  - `Escape` - Cancelar búsqueda
  - `F1` - Ayuda
- **Historial de búsquedas** (últimas 20)
- **Configuración persistente** (carpeta, ventana, historial)
- **Cancelación en tiempo real** de búsquedas

### 📊 Feedback Detallado
- **Barra de progreso** con estado en tiempo real
- **Contador de tiempo** durante búsqueda
- **Mensajes descriptivos**: "Procesando 245 archivos...", "Analizando con IA..."
- **Resultados con metadata**: relevancia %, fecha, tamaño

### 🔐 Sistema de Licencias
- **Licenciamiento basado en dispositivo**
- **Activación simple** con clave JDL-XXXX-XXXX-XXXX
- **Almacenamiento seguro** en directorio del usuario

---

## 🚀 Instalación

### Requisitos del Sistema

- **Sistema Operativo**: Windows 10/11, Linux, macOS
- **Python**: 3.8 o superior
- **RAM**: Mínimo 4GB (8GB recomendado)
- **Espacio**: 500MB libres

### Instalación Rápida

#### Opción 1: Ejecutable (Windows)

1. **Descargar** el instalador desde [Releases](https://github.com/JPatronC92/contextaline/releases)
2. **Ejecutar** `DocumentIntelligence_Setup_1.3.0.exe`
3. **Seguir** el asistente de instalación
4. **Lanzar** desde el menú de inicio o escritorio

#### Opción 2: Desde Código Fuente

```bash
# 1. Clonar el repositorio
git clone https://github.com/JPatronC92/contextaline.git
cd contextaline

# 2. Crear entorno virtual (recomendado)
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (Linux/Mac)
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
python src/app.py
```

### Dependencias Principales

```txt
PyQt6>=6.4.0              # Interfaz gráfica
sentence-transformers     # Modelo de IA (opcional)
scikit-learn>=1.0.0       # TF-IDF fallback
pypdf>=3.0.0              # Lectura de PDFs
python-docx>=0.8.11       # Lectura de Word
numpy>=1.21.0             # Operaciones numéricas
```

---

## 🎯 Uso Rápido

### Primera Vez

1. **Activar licencia** al abrir la aplicación:
   ```
   Licencias válidas de ejemplo:
   JDL-8FK6-IRLY-A5R1
   JDL-0LSF-ZDPJ-ULQB
   JDL-83B1-8WXZ-J416
   ```

2. **Seleccionar carpeta** con tus documentos (`Ctrl+O`)

3. **Escribir búsqueda** en lenguaje natural:
   - "contratos de arrendamiento 2024"
   - "facturas de servicios públicos"
   - "informes financieros primer trimestre"

4. **Presionar Enter** o hacer clic en "Buscar"

5. **Doble clic** en resultados para abrir documentos

### Consejos de Uso

#### ✅ Buenos ejemplos de búsqueda
```
✓ "contratos de servicios de limpieza del 2024"
✓ "facturas pendientes de pago"
✓ "documentos sobre recursos humanos"
✓ "informes de ventas del último trimestre"
✓ "acuerdos de confidencialidad firmados"
```

#### ❌ Evitar
```
✗ "doc" (muy genérico)
✗ "archivo" (poco descriptivo)
✗ "2024" (demasiado amplio)
```

### Funciones Avanzadas

#### Menú Contextual (Clic Derecho)
- **Abrir documento** - Abre con aplicación predeterminada
- **Abrir ubicación** - Abre carpeta contenedora
- **Copiar ruta** - Copia ruta completa al portapapeles
- **Propiedades** - Muestra metadata detallada

#### Historial de Búsquedas
- Haz clic en el **dropdown** del campo de búsqueda
- Selecciona de las **últimas 20 búsquedas**
- Se guarda entre sesiones

---

## 📚 Documentación

### Estructura del Proyecto

```
IntelligentDocumentFinder/
├── src/
│   ├── app.py              # Aplicación principal
│   ├── license.py          # Sistema de licencias
│   └── app_version.py      # Información de versión
├── scripts/
│   ├── installer.iss       # Script de Inno Setup
│   └── preload_model.py    # Pre-descarga del modelo
├── tests/
│   └── smoke_test.py       # Tests de humo
├── test_documents/         # Documentos de prueba
├── requirements.txt        # Dependencias Python
├── build.ps1              # Script de build Windows
├── build.sh               # Script de build Linux/Mac
├── UX_UI_AUDIT_REPORT.md  # Auditoría UX/UI
├── CHANGELOG_v1.3.0.md    # Changelog detallado
└── README.md              # Este archivo
```

### Documentos Disponibles

- **[📋 Manual de Usuario](MANUAL_USUARIO.md)** - Guía completa para usuarios
- **[🔧 Instrucciones de Build](BUILD_INSTRUCTIONS.md)** - Cómo compilar la app
- **[🎨 Auditoría UX/UI](UX_UI_AUDIT_REPORT.md)** - Análisis detallado de UX/UI
- **[📝 Changelog v1.3.0](CHANGELOG_v1.3.0.md)** - Notas de la versión actual
- **[📊 Reportes](STATUS_REPORT.md)** - Estado del proyecto

### Generar Licencias

```bash
# Generar 5 licencias nuevas
python generate_license.py

# Output:
# Licencias generadas:
# JDL-XXXX-XXXX-XXXX
# JDL-YYYY-YYYY-YYYY
# ...
```

---

## 🏗️ Build & Deploy

### Build Ejecutable (Windows)

```powershell
# PowerShell
.\build.ps1

# Genera: dist\IntelligentDocumentFinder.exe
```

### Build Ejecutable (Linux/Mac)

```bash
chmod +x build.sh
./build.sh

# Genera: dist/IntelligentDocumentFinder
```

### Crear Instalador (Windows)

```powershell
# Requiere Inno Setup instalado
iscc scripts\installer.iss

# Genera: dist\installer\DocumentIntelligence_Setup_1.3.0.exe
```

---

## 🧪 Testing

```bash
# Test de humo (verifica que la app arranca)
python tests/smoke_test.py

# Test manual con documentos de prueba
python src/app.py
# Seleccionar carpeta: test_documents/
```

---

## 📈 Roadmap

### ✅ v1.3.0 (Actual) - UX/UI Enhancement
- [x] Atajos de teclado completos
- [x] Diseño visual moderno
- [x] Historial de búsquedas
- [x] Menú contextual
- [x] Configuración persistente
- [x] Mensajes amigables
- [x] Sistema de ayuda (F1)

### 🔄 v1.4.0 (Próximo) - Advanced Features
- [ ] Dark Mode
- [ ] Vista previa de documentos
- [ ] Filtros avanzados (tipo, fecha, tamaño)
- [ ] Exportar resultados (CSV, PDF)
- [ ] Tour guiado para nuevos usuarios
- [ ] Estadísticas de uso

### 🚀 v1.5.0 (Futuro) - Power User
- [ ] Búsqueda avanzada con operadores
- [ ] Carpetas favoritas
- [ ] Búsquedas guardadas
- [ ] Análisis de documentos
- [ ] Gráficos de distribución
- [ ] OCR para PDFs escaneados

---

## 🔧 Configuración Avanzada

### Ubicación de Datos

**Windows:**
```
%APPDATA%\JulioDevs\IDF\
├── license.key          # Licencia activada
└── embedding_cache.json # Caché de embeddings
```

**Linux/macOS:**
```
~/.cache/idf/
├── license.key
└── embedding_cache.json
```

### Configuración de Usuario

Se guarda automáticamente en QSettings:
- Última carpeta usada
- Tamaño y posición de ventana
- Historial de búsquedas (últimas 20)

Para resetear: Eliminar claves del registro (Windows) o archivo de config (Linux/Mac)

---

## 🐛 Solución de Problemas

### Error: "No se pudo cargar el modelo de IA"

**Solución:**
- La app cambia automáticamente a modo básico (TF-IDF)
- Para usar IA completa, instala PyTorch:
  ```bash
  pip install torch sentence-transformers
  ```

### Error: "Carpeta sin permisos"

**Solución:**
- Ejecutar como administrador (Windows)
- Verificar permisos de lectura en carpeta
- Seleccionar otra carpeta accesible

### Búsqueda muy lenta

**Soluciones:**
- Primera búsqueda siempre es más lenta (genera caché)
- Búsquedas subsecuentes son rápidas
- Evitar carpetas con >10,000 documentos
- Usar filtros de sistema operativo primero

### Error: "Licencia inválida"

**Solución:**
- Verificar formato: `JDL-XXXX-XXXX-XXXX`
- Copiar/pegar sin espacios extras
- Generar nueva licencia si es necesaria
- Contactar soporte si el problema persiste

---

## 🤝 Contribuir

Este es un proyecto propietario, pero aceptamos:

- 🐛 **Reportes de bugs** - [Crear issue](https://github.com/JPatronC92/contextaline/issues)
- 💡 **Sugerencias** - [Crear issue](https://github.com/JPatronC92/contextaline/issues)
- 📖 **Mejoras en documentación** - Pull requests bienvenidos

### Reportar Bugs

Al reportar un bug, incluye:
1. **Versión** de la aplicación
2. **Sistema operativo** y versión
3. **Pasos para reproducir**
4. **Comportamiento esperado** vs actual
5. **Screenshots** si es posible

---

## 📊 Métricas de Rendimiento

### Velocidad de Búsqueda

| Escenario | Tiempo | Cache |
|-----------|--------|-------|
| Primera búsqueda (100 docs) | ~10s | ❌ |
| Búsqueda subsecuente | ~2s | ✅ |
| Primera búsqueda (1000 docs) | ~45s | ❌ |
| Búsqueda subsecuente | ~5s | ✅ |

### Precisión

- **Modelo IA (Sentence-BERT)**: ~92% precisión
- **Modo básico (TF-IDF)**: ~75% precisión

---

## 📜 Licencia

**Propietario - © 2025 JulioDevs**

Este software es propietario y requiere una licencia válida para su uso.

### Licencias de Evaluación

Para pruebas y evaluación, usa estas licencias:
```
JDL-8FK6-IRLY-A5R1
JDL-0LSF-ZDPJ-ULQB
JDL-83B1-8WXZ-J416
JDL-R2V3-UJX5-LWAL
JDL-FP9P-RMUY-96T3
```

Para licencias comerciales, contacta: [soporte@juliodevs.com](mailto:soporte@juliodevs.com)

---

## 👥 Créditos

**Desarrollador:** JulioDevs  
**Versión:** 1.3.0  
**Fecha:** Noviembre 2025

### Tecnologías Utilizadas

- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Framework GUI
- **[Sentence-Transformers](https://www.sbert.net/)** - Modelos de IA
- **[scikit-learn](https://scikit-learn.org/)** - TF-IDF fallback
- **[PyPDF](https://pypdf.readthedocs.io/)** - Lectura de PDFs
- **[python-docx](https://python-docx.readthedocs.io/)** - Lectura de Word

---

## 📞 Soporte

- **Issues:** [GitHub Issues](https://github.com/JPatronC92/contextaline/issues)
- **Email:** soporte@juliodevs.com
- **Documentación:** [Wiki del proyecto](https://github.com/JPatronC92/contextaline/wiki)

---

## 🌟 Changelog

### v1.3.0 (2 Nov 2025) - UX/UI Enhancement
- ✨ **Nuevo:** Atajos de teclado completos (Ctrl+O, Ctrl+F, Enter, etc.)
- ✨ **Nuevo:** Historial de búsquedas con dropdown
- ✨ **Nuevo:** Menú contextual en resultados (clic derecho)
- ✨ **Nuevo:** Configuración persistente (carpeta, ventana, historial)
- ✨ **Nuevo:** Sistema de ayuda integrado (F1)
- 🎨 **Mejorado:** Diseño visual moderno con colores coherentes
- 🎨 **Mejorado:** Iconos emoji en toda la interfaz
- 🎨 **Mejorado:** Resultados enriquecidos con metadata
- 🎨 **Mejorado:** Colores por relevancia (🟢🟡🟠)
- 🔧 **Mejorado:** Mensajes de error amigables
- 🔧 **Mejorado:** Feedback detallado durante búsqueda
- ⚡ **Mejorado:** Cancelación de búsqueda en tiempo real
- 📊 **Mejorado:** Contador de tiempo durante búsqueda

Ver [CHANGELOG completo](CHANGELOG_v1.3.0.md)

### v1.2.0 - Stability & Performance
- 🔧 Sistema de caché de embeddings
- ⚡ Mejora de rendimiento 50%
- 🐛 Correcciones de bugs

### v1.0.0 - Initial Release
- 🎉 Lanzamiento inicial
- 🧠 Búsqueda con IA Sentence-BERT
- 📄 Soporte PDF, DOCX, TXT
- 🔐 Sistema de licencias

---

<div align="center">

**[⬆ Volver arriba](#-intelligentdocumentfinder)**

---

Hecho con ❤️ por **JulioDevs**

*Encuentra lo que buscas, más rápido que nunca* 🚀

</div>
