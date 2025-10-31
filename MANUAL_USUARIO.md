# 📖 Manual de Usuario - IntelligentDocumentFinder

## 🎯 ¿Qué es IntelligentDocumentFinder?

Es una aplicación de escritorio que utiliza Inteligencia Artificial para buscar documentos de manera inteligente. En lugar de buscar solo por nombre de archivo, busca por **contenido y similitud semántica**.

---

## 🚀 Cómo Usar la Aplicación

### 1️⃣ **Primer Inicio - Activación de Licencia**

Al abrir la aplicación por primera vez, se te pedirá una licencia:

**Licencias válidas generadas:**
```
JDL-8FK6-IRLY-A5R1
JDL-0LSF-ZDPJ-ULQB
JDL-83B1-8WXZ-J416
JDL-R2V3-UJX5-LWAL
JDL-FP9P-RMUY-96T3
```

- Copia cualquiera de estas licencias
- Pégala en el cuadro de diálogo
- Haz clic en "OK"
- La licencia se guardará y no volverá a pedirse

---

### 2️⃣ **Seleccionar Carpeta de Documentos**

1. Haz clic en el botón **"Seleccionar Carpeta"**
2. Navega hasta la carpeta que contiene tus documentos
3. Selecciona la carpeta
4. Verás la ruta de la carpeta seleccionada

**Formatos soportados:**
- 📄 PDF (`.pdf`)
- 📝 Word (`.docx`, `.doc`)
- 📃 Texto plano (`.txt`)

---

### 3️⃣ **Realizar una Búsqueda**

1. **Escribe tu consulta** en el campo de búsqueda
   
   **Ejemplos de búsquedas:**
   - "contratos de arrendamiento del año 2024"
   - "facturas de servicios públicos"
   - "informes financieros del primer trimestre"
   - "documentos sobre recursos humanos"
   - "acuerdos de confidencialidad"

2. **Haz clic en "Buscar"**
   - Verás una barra de progreso mientras busca
   - El proceso puede tardar según la cantidad de documentos

3. **Revisa los resultados**
   - Se mostrarán los documentos más relevantes
   - Cada resultado muestra:
     * Nombre del archivo
     * Score de similitud (0.0 a 1.0)
     * Ruta completa

---

### 4️⃣ **Abrir un Documento**

- **Doble clic** sobre cualquier resultado
- El documento se abrirá con su aplicación predeterminada

---

## 🧠 ¿Cómo Funciona la IA?

La aplicación usa un modelo de lenguaje natural llamado **"all-MiniLM-L6-v2"** que:

1. **Lee el contenido** de todos tus documentos
2. **Entiende el significado** de tu búsqueda
3. **Compara semánticamente** tu consulta con el contenido
4. **Ordena los resultados** por relevancia

**Ventaja:** No necesitas saber el nombre exacto del archivo. La IA entiende el contexto y encuentra documentos relacionados aunque uses palabras diferentes.

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Búsqueda de Contratos
```
Consulta: "contratos de servicios de limpieza"
Resultados posibles:
- contrato_limpieza_2024.pdf (Score: 0.892)
- acuerdo_servicios_generales.docx (Score: 0.756)
- propuesta_mantenimiento.pdf (Score: 0.643)
```

### Ejemplo 2: Búsqueda de Facturas
```
Consulta: "facturas de electricidad agosto"
Resultados posibles:
- factura_agosto_2024.pdf (Score: 0.945)
- recibo_luz_08-2024.pdf (Score: 0.887)
- servicios_publicos_verano.docx (Score: 0.621)
```

### Ejemplo 3: Búsqueda de Informes
```
Consulta: "reporte de ventas del trimestre"
Resultados posibles:
- informe_Q3_ventas.docx (Score: 0.912)
- analisis_comercial_septiembre.pdf (Score: 0.834)
- estadisticas_tercer_trimestre.xlsx (Score: 0.789)
```

---

## ⚙️ Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11
- **RAM:** Mínimo 4 GB (recomendado 8 GB)
- **Espacio en Disco:** ~500 MB para la aplicación
- **Procesador:** Intel Core i3 o equivalente

---

## ❓ Preguntas Frecuentes

### ¿Por qué tarda tanto la primera búsqueda?
La primera vez que usas la aplicación después de abrirla, el modelo de IA se carga en memoria. Esto puede tardar 30-60 segundos. Las búsquedas siguientes serán más rápidas.

### ¿Cuántos documentos puede procesar?
La aplicación puede manejar miles de documentos, pero el tiempo de búsqueda aumenta con la cantidad. Para mejores resultados, organiza tus documentos por categorías en carpetas diferentes.

### ¿La búsqueda funciona offline?
Sí, completamente. Una vez instalada, no requiere conexión a internet.

### ¿Dónde se guarda mi licencia?
En Windows: `%APPDATA%\JulioDevs\IDF\license.key`

### ¿Puedo generar más licencias?
Sí, ejecuta el archivo `generate_license.py` en el directorio de instalación:
```powershell
python generate_license.py
```

---

## 🐛 Solución de Problemas

### La aplicación no inicia
- Verifica que no haya otro antivirus bloqueándola
- Ejecuta como administrador

### No encuentra documentos
- Verifica que la carpeta seleccionada contenga archivos PDF, DOCX o TXT
- Asegúrate de que los archivos no estén corruptos

### Los resultados no son relevantes
- Intenta ser más específico en tu búsqueda
- Usa oraciones completas en lugar de palabras sueltas
- Ejemplo: ❌ "contrato" → ✅ "contrato de servicios de limpieza"

---

## 📧 Soporte

Para generar nuevas licencias o asistencia técnica, ejecuta:
```powershell
python generate_license.py
```

---

## 📄 Licencia y Derechos

**IntelligentDocumentFinder v1.0**  
© 2025 JulioDevs  
Todos los derechos reservados.

---

**¡Gracias por usar IntelligentDocumentFinder!** 🎉
