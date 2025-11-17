# Herramientas de Calidad y Seguridad

**Guía completa de herramientas para mantener calidad y seguridad en el proyecto**

---

## 📋 Tabla de Contenidos

1. [Instalación](#instalación)
2. [Testing](#testing)
3. [Calidad de Código](#calidad-de-código)
4. [Seguridad](#seguridad)
5. [Pre-Commit](#pre-commit)
6. [Scripts de PowerShell](#scripts-de-powershell)

---

## 🔧 Instalación

### Instalar todas las herramientas de desarrollo:

```powershell
# UBICACIÓN: Raíz del proyecto (C:\workspace\seed-proyect)

pip install -r requirements-dev.txt
```

**Qué instala:**
- **Testing:** pytest, pytest-cov, pytest-mock, pytest-watch
- **Calidad:** pylint, flake8, mypy, black, isort, radon
- **Seguridad:** pip-audit, bandit, safety
- **Debugging:** ipdb, ipython

---

## 🧪 Testing

### Comandos básicos:

```powershell
# UBICACIÓN: Raíz del proyecto

# Todos los tests
pytest tests/ -v

# Solo unitarios (rápidos - para TDD)
pytest tests/ -v -m unit

# Solo integración
pytest tests/ -v -m integration

# Solo e2e
pytest tests/ -v -m e2e

# Watch mode (TDD continuo)
ptw tests/unit/
```

### Con cobertura:

```powershell
# Cobertura básica
pytest tests/ --cov=app

# Cobertura con reporte HTML
pytest tests/ --cov=app --cov-report=html
# Ver en: htmlcov/index.html

# Cobertura mostrando líneas faltantes
pytest tests/ --cov=app --cov-report=term-missing

# Fallar si cobertura < 80%
pytest tests/ --cov=app --cov-fail-under=80
```

### Tests específicos:

```powershell
# Por nombre
pytest tests/ -k "test_create_user"

# Test específico
pytest tests/unit/test_user_entity.py::test_user_creation

# Con output de print
pytest tests/ -v -s

# Con debugger on failure
pytest tests/ -v --pdb
```

---

## 🎨 Calidad de Código

### Pylint (Linting):

```powershell
# UBICACIÓN: Raíz del proyecto

# Analizar todo el código
pylint app/

# Con score mínimo requerido (8.0)
pylint app/ --fail-under=8.0

# Solo errores críticos
pylint app/ --errors-only

# Con formato parseable
pylint app/ --output-format=parseable
```

**Qué verifica:**
- Errores de sintaxis y lógica
- Convenciones de nombres
- Imports sin usar
- Complejidad de funciones
- Duplicación de código

**Score objetivo:** ≥ 8.0/10

### Flake8 (Style):

```powershell
# Verificar estilo
flake8 app/

# Con longitud de línea específica
flake8 app/ --max-line-length=100

# Mostrar estadísticas
flake8 app/ --statistics

# Por archivo
flake8 app/domain/entities/user.py
```

**Qué verifica:**
- PEP 8 style guide
- Complejidad ciclomática (< 10)
- Longitud de línea (100 chars)
- Espaciado y formato

### Black (Auto-format):

```powershell
# Verificar sin modificar
black app/ --check

# Formatear código
black app/

# Ver diferencias
black app/ --diff

# Formatear archivo específico
black app/domain/entities/user.py
```

**Qué hace:**
- Formateo automático consistente
- Ajusta espaciado, indentación
- Organiza imports
- Longitud de línea (100 chars)

### Isort (Import sorting):

```powershell
# Verificar sin modificar
isort app/ --check-only

# Ordenar imports
isort app/

# Ver diferencias
isort app/ --diff

# Por archivo
isort app/domain/entities/user.py
```

**Qué hace:**
- Ordena imports: stdlib → third-party → local
- Agrupa imports relacionados
- Elimina imports duplicados

### Mypy (Type checking):

```powershell
# Verificar tipos
mypy app/

# Modo estricto
mypy app/ --strict

# Por módulo
mypy app/domain/
```

**Qué verifica:**
- Anotaciones de tipos
- Consistencia de tipos
- Errores de tipo en runtime

### Radon (Complejidad):

```powershell
# Complejidad ciclomática
radon cc app/ -a -nb

# Índice de mantenibilidad
radon mi app/ -nb

# Raw metrics (LOC, etc.)
radon raw app/ -s
```

**Qué mide:**
- Complejidad ciclomática (< 10 objetivo)
- Índice de mantenibilidad (A-F)
- Líneas de código
- Comentarios

---

## 🔒 Seguridad

### Pip-audit (Vulnerabilidades en dependencias):

```powershell
# UBICACIÓN: Raíz del proyecto

# Escanear vulnerabilidades
pip-audit

# Con detalles
pip-audit --desc

# Formato JSON
pip-audit --format json

# Solo severidad alta/crítica
pip-audit --severity high
```

**Qué verifica:**
- Vulnerabilidades conocidas en dependencias
- CVEs publicados
- Versiones afectadas
- Recomendaciones de actualización

### Bandit (Security issues en código):

```powershell
# Escanear código
bandit -r app/

# Con nivel de severidad
bandit -r app/ -ll

# Formato JSON
bandit -r app/ -f json

# Ignorar tests
bandit -r app/ --skip B101
```

**Qué verifica:**
- Credenciales hardcodeadas
- Inyección SQL
- Uso inseguro de funciones
- Problemas de criptografía
- Manejo inseguro de archivos

### Safety (Vulnerabilidades):

```powershell
# Verificar dependencias
safety check

# Con detalles completos
safety check --full-report

# Solo producción
safety check --file requirements.txt
```

---

## ✅ Pre-Commit

### Verificación completa antes de commit:

```powershell
# UBICACIÓN: Raíz del proyecto

# Ejecutar todas las verificaciones
pytest tests/ -v
pytest tests/ --cov=app --cov-fail-under=80
pylint app/ --fail-under=8.0
flake8 app/ --max-line-length=100
black app/ --check
isort app/ --check-only
pip-audit
bandit -r app/
```

### Script automatizado:

```powershell
# Usar script de PowerShell
.\scripts-dev.ps1

# Seleccionar opción 16 (PRE-COMMIT COMPLETO)
```

**Qué verifica:**
1. ✅ Todos los tests pasan
2. ✅ Cobertura ≥ 80%
3. ✅ Pylint ≥ 8.0
4. ✅ Flake8 sin errores
5. ✅ Black formateado
6. ✅ Imports ordenados
7. ✅ Sin vulnerabilidades
8. ✅ Sin issues de seguridad

---

## 🖥️ Scripts de PowerShell

### Uso del script interactivo:

```powershell
# UBICACIÓN: Raíz del proyecto

.\scripts-dev.ps1
```

**Opciones disponibles:**

| Opción | Descripción |
|--------|-------------|
| 1 | Ejecutar TODOS los tests |
| 2 | Solo tests unitarios (rápidos) |
| 3 | Solo tests de integración |
| 4 | Solo tests e2e |
| 5 | Tests con cobertura HTML |
| 6 | Tests con cobertura (fail < 80%) |
| 7 | Watch mode (TDD) |
| 8 | Ejecutar pylint |
| 9 | Ejecutar flake8 |
| 10 | Black (check) |
| 11 | Black (format) |
| 12 | Isort (check) |
| 13 | Isort (format) |
| 14 | Pip-audit (seguridad) |
| 15 | Bandit (seguridad) |
| 16 | **PRE-COMMIT COMPLETO** |
| 17 | Instalar dependencias dev |
| 18 | Iniciar servidor FastAPI |

---

## 📊 Resumen de Métricas

### Objetivos de calidad:

| Métrica | Objetivo | Herramienta |
|---------|----------|-------------|
| **Cobertura de tests** | ≥ 80% | pytest-cov |
| **Pylint score** | ≥ 8.0/10 | pylint |
| **Complejidad ciclomática** | < 10 | radon, flake8 |
| **Duplicación de código** | < 3% | pylint |
| **Vulnerabilidades** | 0 | pip-audit, bandit |
| **Funciones** | ≤ 50 líneas | radon |
| **Líneas por archivo** | ≤ 500 (ideal) | radon |

---

## 🚀 Workflow Recomendado

### Durante desarrollo (TDD):

```powershell
# 1. Activar watch mode
ptw tests/unit/

# 2. Escribir test (RED)
# 3. Escribir código (GREEN)
# 4. Refactorizar (REFACTOR)
# 5. Repetir
```

### Antes de commit:

```powershell
# Opción 1: Manual
pytest tests/ -v
pytest tests/ --cov=app --cov-fail-under=80
pylint app/ --fail-under=8.0
black app/ --check
isort app/ --check-only

# Opción 2: Script automatizado
.\scripts-dev.ps1
# Seleccionar opción 16
```

### Después de pull:

```powershell
# Verificar todo funciona
pytest tests/ -v
pip-audit
```

---

## 🔧 Troubleshooting

### Problema: pytest no encuentra módulos

**Solución:**
```powershell
# Asegurarse de tener __init__.py en todas las carpetas
# O agregar al PYTHONPATH
$env:PYTHONPATH = "C:\workspace\seed-proyect"
```

### Problema: black y flake8 en conflicto

**Solución:** Ya está configurado en `.flake8`:
- Ignora E203, W503 (conflictos conocidos con black)

### Problema: pylint score muy bajo

**Solución:**
```powershell
# Ver qué está bajando el score
pylint app/ --output-format=parseable

# Ignorar mensajes específicos en .pylintrc
```

### Problema: pip-audit encuentra vulnerabilidades

**Solución:**
```powershell
# Ver detalles
pip-audit --desc

# Actualizar dependencias
pip install --upgrade <paquete>

# Verificar nuevamente
pip-audit
```

---

## 📚 Referencias

- [Pytest Documentation](https://docs.pytest.org/)
- [Pylint User Guide](https://pylint.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Pip-audit Documentation](https://pypi.org/project/pip-audit/)

---

**Última actualización:** 2025-11-17

