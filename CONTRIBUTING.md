# Guía de Contribución

¡Gracias por tu interés en contribuir a IntelligentDocumentFinder! 🎉

## 📋 Formas de Contribuir

Aunque este es un proyecto propietario, aceptamos contribuciones en las siguientes áreas:

### 🐛 Reportar Bugs

1. **Verifica** que el bug no esté ya reportado en [Issues](https://github.com/JPatronC92/contextaline/issues)
2. **Crea** un nuevo issue con el template de bug
3. **Incluye**:
   - Versión de la aplicación
   - Sistema operativo
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Screenshots si es posible

### 💡 Proponer Features

1. **Busca** si la feature ya fue propuesta
2. **Crea** un issue con el template de feature request
3. **Describe**:
   - El problema que resuelve
   - Cómo mejoraría la experiencia
   - Casos de uso específicos

### 📖 Mejorar Documentación

1. **Fork** el repositorio
2. **Edita** los archivos .md necesarios
3. **Crea** un Pull Request
4. Documentación aceptada:
   - Correcciones de typos
   - Mejoras en README
   - Traducciones
   - Ejemplos de uso
   - Guías de troubleshooting

## 🔧 Desarrollo

### Setup del Entorno

```bash
# 1. Fork y clonar
git clone https://github.com/TU_USUARIO/contextaline.git
cd contextaline

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar tests
python tests/smoke_test.py
```

### Estándares de Código

- **Python 3.8+**
- **PEP 8** style guide
- **Type hints** cuando sea posible
- **Docstrings** en funciones públicas
- **Comentarios** en código complejo

### Git Workflow

```bash
# 1. Crear rama
git checkout -b feature/mi-feature

# 2. Hacer cambios
git add .
git commit -m "feat: descripción del cambio"

# 3. Push y PR
git push origin feature/mi-feature
```

### Convenciones de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: nueva característica
fix: corrección de bug
docs: cambios en documentación
style: formato, punto y coma, etc
refactor: refactorización de código
test: agregar tests
chore: mantenimiento
```

Ejemplos:
```bash
git commit -m "feat: add dark mode toggle"
git commit -m "fix: resolve search crash on empty query"
git commit -m "docs: update installation instructions"
```

## ✅ Checklist para Pull Requests

Antes de enviar un PR, verifica:

- [ ] El código sigue el style guide del proyecto
- [ ] Los tests pasan correctamente
- [ ] La documentación está actualizada
- [ ] Los commits siguen convenciones
- [ ] El PR tiene una descripción clara
- [ ] No hay archivos temporales o de build

## 📝 Template de Pull Request

```markdown
## Descripción
[Breve descripción del cambio]

## Tipo de cambio
- [ ] Bug fix
- [ ] Nueva feature
- [ ] Breaking change
- [ ] Documentación

## ¿Cómo se ha probado?
[Describe las pruebas realizadas]

## Checklist
- [ ] Mi código sigue el style guide
- [ ] He actualizado la documentación
- [ ] He agregado tests
- [ ] Los tests pasan
```

## 🔍 Proceso de Revisión

1. **Automático**: CI/CD verifica formato y tests
2. **Manual**: Mantenedores revisan el código
3. **Feedback**: Se solicitan cambios si es necesario
4. **Merge**: Se acepta el PR si todo está correcto

Tiempo estimado de revisión: **2-5 días hábiles**

## 💬 Comunicación

- **Issues**: Para bugs y features
- **Discussions**: Para preguntas generales
- **Email**: soporte@juliodevs.com para temas privados

## 🎯 Prioridades Actuales

Ver [Roadmap en README](README.md#-roadmap) para:
- Features en desarrollo
- Áreas que necesitan ayuda
- Prioridades del proyecto

## 📚 Recursos

- [README](README.md) - Información general
- [Manual de Usuario](MANUAL_USUARIO.md) - Guía completa
- [UX/UI Audit](UX_UI_AUDIT_REPORT.md) - Análisis de UX
- [Changelog](CHANGELOG_v1.3.0.md) - Historial de cambios

## 🙏 Agradecimientos

¡Gracias por contribuir a IntelligentDocumentFinder! Tu aporte hace mejor el proyecto para todos.

---

**¿Dudas?** Abre un issue con la etiqueta `question` o contacta a soporte@juliodevs.com
