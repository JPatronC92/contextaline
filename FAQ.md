# ❓ Preguntas Frecuentes (FAQ)

## 📋 Índice

- [General](#general)
- [Instalación](#instalación)
- [Uso](#uso)
- [Licencias](#licencias)
- [Problemas Técnicos](#problemas-técnicos)
- [Performance](#performance)
- [Privacidad y Seguridad](#privacidad-y-seguridad)

---

## General

### ¿Qué hace IntelligentDocumentFinder?

Es un buscador inteligente que utiliza IA para encontrar documentos por contenido y significado, no solo por nombre de archivo.

### ¿Qué formatos de archivo soporta?

- **PDF** (`.pdf`)
- **Word** (`.docx`, `.doc`)
- **Texto plano** (`.txt`)

### ¿Funciona sin conexión a internet?

Sí, funciona **100% offline**. La IA se ejecuta localmente en tu computadora.

### ¿En qué plataformas funciona?

- **Windows** 10/11 ✅
- **Linux** (Ubuntu, Debian, etc.) ✅
- **macOS** 10.15+ ✅

---

## Instalación

### ¿Cuánto espacio necesita?

- **Instalación**: ~200MB
- **Con modelo IA**: ~500MB
- **Modo básico**: ~50MB

### ¿Necesito Python instalado?

- **Ejecutable (Windows)**: No, viene todo incluido
- **Desde código fuente**: Sí, Python 3.8+

### ¿Cómo actualizo a la última versión?

1. Desinstala la versión anterior
2. Descarga e instala la nueva versión
3. Tu licencia y configuración se mantienen

### Error: "No se puede instalar en Windows"

**Soluciones:**
- Ejecutar instalador como administrador
- Desactivar antivirus temporalmente
- Verificar que Windows esté actualizado

---

## Uso

### ¿Cómo escribo una buena búsqueda?

**✅ Buenos ejemplos:**
```
"contratos de servicios de limpieza del 2024"
"facturas pendientes de pago de proveedores"
"informes financieros del primer trimestre"
```

**❌ Evitar:**
```
"doc" (muy genérico)
"2024" (demasiado amplio)
```

**Tip:** Describe en lenguaje natural lo que buscas.

### ¿Puedo buscar en múltiples carpetas?

Actualmente, una carpeta a la vez. Pero puedes:
- Seleccionar una carpeta padre que contenga subcarpetas
- La búsqueda es recursiva (busca en subcarpetas)

### ¿Por qué no encuentra un documento que sé que existe?

Posibles razones:
1. **Formato no soportado** (solo PDF, DOCX, TXT)
2. **Documento vacío** o solo con imágenes (PDF escaneado)
3. **Términos muy diferentes** a los del contenido
4. **Archivo dañado** o corrupto

### ¿Cómo uso los atajos de teclado?

- `Ctrl+O` - Abrir carpeta
- `Ctrl+F` - Enfocar búsqueda
- `Enter` - Buscar
- `Ctrl+R` - Limpiar resultados
- `Escape` - Cancelar búsqueda
- `F1` - Ayuda completa

---

## Licencias

### ¿Necesito internet para activar la licencia?

No, la activación es **completamente offline**.

### ¿Puedo usar la licencia en múltiples computadoras?

No, cada licencia es para **un dispositivo** específico.

### ¿Qué pasa si cambio de computadora?

Contacta a soporte@juliodevs.com para transferir tu licencia.

### Perdí mi licencia, ¿qué hago?

1. Revisa el email de compra
2. Si no lo encuentras, contacta a soporte con tu información de compra

### ¿Hay licencias de prueba?

Sí, para evaluación usa estas licencias:
```
JDL-8FK6-IRLY-A5R1
JDL-0LSF-ZDPJ-ULQB
JDL-83B1-8WXZ-J416
```

---

## Problemas Técnicos

### Error: "No se pudo cargar el modelo de IA"

**No es un error crítico.** La app cambia automáticamente a modo básico (TF-IDF).

Para usar IA completa:
```bash
pip install torch sentence-transformers
```

### La búsqueda es muy lenta

**Primera búsqueda**: Es normal, genera caché (puede tardar 30-60s)
**Búsquedas siguientes**: Deben ser rápidas (2-5s)

**Si sigue lento:**
- Carpeta con demasiados archivos (>10,000)
- PC con poca RAM (<4GB)
- Archivos muy grandes (>100MB cada uno)

### Error: "Carpeta sin permisos"

**Windows:**
1. Clic derecho en carpeta → Propiedades → Seguridad
2. Verificar permisos de lectura

**Linux/Mac:**
```bash
chmod -R +r /ruta/a/carpeta
```

### La aplicación no abre

1. **Verificar** que no esté ya ejecutándose (Task Manager)
2. **Ejecutar** como administrador
3. **Revisar** logs en `%APPDATA%\JulioDevs\IDF\`
4. **Reinstalar** si persiste

### Los resultados no son relevantes

En **Modo Básico (TF-IDF)**:
- Precisión ~75%
- Usa palabras clave exactas

En **Modo IA (Sentence-BERT)**:
- Precisión ~92%
- Entiende sinónimos y contexto

**Solución:** Instalar modelo IA completo.

---

## Performance

### ¿Cuántos documentos puede manejar?

- **Óptimo**: 100-1,000 documentos
- **Funcional**: 1,000-10,000 documentos
- **Posible**: 10,000+ (puede ser lento)

### ¿Puedo acelerar las búsquedas?

Sí:
1. **Primera vez**: Deja que genere caché completo
2. **Mantén caché**: No borres `embedding_cache.json`
3. **Organiza**: Usa subcarpetas específicas
4. **Hardware**: Más RAM = más rápido

### ¿Qué hace el caché?

Guarda los "embeddings" (representaciones IA) de documentos ya procesados. Así no tiene que reprocesarlos cada vez.

**Ubicación:**
- Windows: `%APPDATA%\JulioDevs\IDF\embedding_cache.json`
- Linux/Mac: `~/.cache/idf/embedding_cache.json`

### ¿Puedo borrar el caché?

Sí, es seguro. Se regenerará en la próxima búsqueda (será más lenta).

---

## Privacidad y Seguridad

### ¿Envían mis documentos a algún servidor?

**No.** Todo se procesa **100% localmente** en tu computadora.

### ¿Recopilan datos de uso?

**No.** No hay telemetría ni tracking.

### ¿Es seguro introducir mi licencia?

Sí, la licencia se valida **offline** y se guarda **localmente**.

### ¿Qué información se almacena?

Solo:
- Licencia (cifrada)
- Última carpeta usada
- Historial de búsquedas (últimas 20)
- Tamaño de ventana
- Caché de embeddings

**Todo almacenado localmente.**

### ¿Puedo usar en documentos confidenciales?

Sí, es **100% seguro**. Nada sale de tu computadora.

### ¿Es open source?

Es **propietario**, pero aceptamos contribuciones en:
- Reportes de bugs
- Sugerencias de features
- Mejoras en documentación

---

## 🤔 ¿Más Preguntas?

- **Issues**: [GitHub Issues](https://github.com/JPatronC92/contextaline/issues)
- **Email**: soporte@juliodevs.com
- **Docs**: [README](README.md) | [Manual](MANUAL_USUARIO.md)

---

**Última actualización**: Noviembre 2025 - v1.3.0
