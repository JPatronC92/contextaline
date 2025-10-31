# Instrucciones de Construcción - IntelligentDocumentFinder

## 📋 Resumen del Estado

✅ **Completado:**
- Estructura completa del proyecto
- Código fuente de la aplicación
- Sistema de licencias
- Scripts de construcción
- Descarga del modelo ML (all-MiniLM-L6-v2)

⏳ **En Proceso:**
- Generación del ejecutable final (.exe)

## 🔧 Cambios Implementados para Resolver el Problema de Empaquetado

### Problema Identificado
PyInstaller se interrumpía durante la compresión debido al alto consumo de recursos al procesar librerías pesadas (torch, scikit-learn).

### Soluciones Aplicadas

1. **Modo `--onefile` por defecto**
   - Ahora el script usa `--onefile` sin necesidad de parámetros
   - Genera un único .exe más fácil de distribuir
   - Mejor manejo de procesos largos

2. **Compresión UPX deshabilitada (`--noupx`)**
   - UPX es la principal causa de timeouts
   - El .exe será más grande pero se generará más rápido
   - Deshabilitado tanto en comando directo como en idf.spec

3. **Mensajes informativos mejorados**
   - El script ahora advierte que el proceso puede tardar
   - Instrucciones claras para no interrumpir

## 🚀 Cómo Construir el Ejecutable

### Opción 1: Construcción Rápida (Recomendada)
```powershell
.\build.ps1
```
- Usa modo `--onefile` sin compresión UPX
- **Tiempo estimado:** 3-7 minutos
- **Resultado:** `dist\IntelligentDocumentFinder.exe` (tamaño ~200-300 MB)

### Opción 2: Con Limpieza Previa
```powershell
.\build.ps1 -Clean
```
- Elimina builds anteriores antes de construir
- Útil si hubo errores previos

### Opción 3: Usando el .spec (Modo Carpeta)
```powershell
.\build.ps1 -UseSpec
```
- Genera una carpeta en `dist\IntelligentDocumentFinder\`
- El ejecutable estará dentro con todas sus dependencias
- **Ventaja:** Más rápido de generar
- **Desventaja:** Menos portable (múltiples archivos)

## ⚠️ IMPORTANTE Durante la Construcción

1. **NO INTERRUMPAS EL PROCESO**
   - Aunque parezca que se detuvo, sigue trabajando
   - La fase de análisis de dependencias puede tardar 2-3 minutos sin output visible
   - La fase final de empaquetado tarda 1-3 minutos adicionales

2. **Monitorea el Uso de Recursos**
   - Abre el Administrador de Tareas
   - Verás `python.exe` con alto uso de CPU (normal)
   - Si el uso de CPU baja a 0% por más de 5 minutos, entonces sí hay un problema

3. **Espera el Mensaje Final**
   - El proceso termina cuando veas: `==> Listo. Revisa /dist` en verde
   - Solo entonces puedes revisar la carpeta `dist`

## 📦 Después de la Construcción Exitosa

### Verificar el Ejecutable
```powershell
# Ver el archivo generado
Get-ChildItem dist\
```

### Probar el Ejecutable
```powershell
# Ejecutar directamente
.\dist\IntelligentDocumentFinder.exe
```

### Crear el Instalador (Paso Final)
Una vez que tengas el `.exe` funcionando:

1. **Requisito:** Instalar Inno Setup
   - Descarga: https://jrsoftware.org/isdl.php
   
2. **Compilar el Instalador:**
   ```powershell
   # Abrir Inno Setup y compilar scripts\installer.iss
   # O desde línea de comandos:
   & "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" scripts\installer.iss
   ```

3. **Resultado:**
   - Instalador generado en `Output\IntelligentDocumentFinder-Setup.exe`

## 🐛 Solución de Problemas

### Si el proceso se interrumpe nuevamente:

1. **Verifica espacio en disco:**
   ```powershell
   Get-PSDrive C | Select-Object Used,Free
   ```
   - Necesitas al menos 3-4 GB libres

2. **Cierra aplicaciones pesadas:**
   - Navegadores con muchas pestañas
   - IDEs adicionales
   - Otros procesos de Python

3. **Construye en modo carpeta primero:**
   ```powershell
   .\build.ps1 -Clean -UseSpec
   ```
   - Es más rápido y confirma que todo funciona
   - Luego prueba el modo `--onefile`

4. **Ejecuta directamente PyInstaller con más verbosidad:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pyinstaller --log-level=INFO --noconfirm --onefile --windowed --noupx src/app.py --name IntelligentDocumentFinder
   ```
   - Verás más detalles del proceso

## 📊 Tiempos Esperados

| Fase | Tiempo Estimado | Señal Visual |
|------|----------------|--------------|
| Creación de venv | 10-30 seg | Output de pip |
| Instalación de dependencias | 2-5 min | Descarga de paquetes |
| Precarga del modelo | 30-90 seg | Descarga del modelo |
| Análisis de PyInstaller | 2-3 min | Output de "Analyzing..." |
| Empaquetado | 1-3 min | Output de "Building..." |
| **TOTAL** | **6-12 min** | - |

## ✅ Checklist Final

- [ ] El script build.ps1 completó sin errores
- [ ] Existe el archivo `dist\IntelligentDocumentFinder.exe`
- [ ] El ejecutable abre la interfaz gráfica
- [ ] La aplicación puede buscar documentos
- [ ] La verificación de licencia funciona
- [ ] Crear el instalador con Inno Setup
- [ ] Probar el instalador en un sistema limpio

## 📞 Próximos Pasos

1. Ejecutar `.\build.ps1` y dejar que termine completamente
2. Verificar que el .exe funciona correctamente
3. Crear el instalador de Windows
4. ¡Proyecto completado! 🎉
