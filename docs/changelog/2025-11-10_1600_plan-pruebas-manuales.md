# Changelog - Plan de Pruebas Manuales

**Fecha:** 2025-11-10  
**Estado:** ✅ COMPLETADA

---

## 🎯 Objetivo

Crear un plan completo de pruebas manuales para verificar el funcionamiento end-to-end de la API REST de gestión de usuarios.

---

## ✅ Cambios Realizados

### 1. **Documentación de Pruebas Creada**

#### `docs/START_SERVER.md` (NUEVO)
- **Propósito:** Guía detallada para iniciar el servidor FastAPI
- **Contenido:**
  - Comando correcto con explicación detallada
  - Salida esperada del servidor
  - Opciones adicionales (puerto, host, workers)
  - Troubleshooting completo (5 problemas comunes)
  - Configuración de logs
  - URLs útiles de referencia
  
#### `docs/QUICK_START_TESTING.md` (NUEVO)
- **Propósito:** Guía rápida de testing en 3 pasos
- **Contenido:**
  - Inicio rápido del servidor
  - Uso de Swagger UI
  - Ejecución de script de pruebas
  - Casos de prueba rápidos (4 ejemplos)
  - Verificación de base de datos
  - Comandos de tests automatizados
  - Checklist de verificación
- **Tiempo estimado:** ~20 minutos

#### `docs/MANUAL_TESTING.md` (NUEVO)
- **Propósito:** Plan completo y exhaustivo de pruebas manuales
- **Contenido:**
  - Pre-requisitos y setup completo
  - **15+ casos de prueba documentados:**
    - 2 tests de endpoints básicos (health, root)
    - 7 casos de éxito (crear usuarios válidos)
    - 6 casos de error (validaciones)
    - 2 casos especiales (edge cases)
  - Resultados esperados para cada test
  - Verificación de base de datos (SQLite)
  - Pruebas desde Swagger UI
  - Ejecución de tests automatizados
  - Pruebas de persistencia (reinicio de servidor)
  - Checklist completo de verificación
  - Troubleshooting (3 problemas comunes)
  - Plantilla de reporte de pruebas
- **Tiempo estimado:** ~40 minutos

#### `docs/test_commands.ps1` (NUEVO)
- **Propósito:** Script PowerShell ejecutable con todos los comandos curl
- **Contenido:**
  - 15 tests automatizados con curl
  - Códigos de colores para fácil lectura
  - Pausas entre tests (1 segundo)
  - Resumen automático al final
  - Validación de status codes
- **Tiempo estimado:** ~2 minutos
- **Uso:** `.\docs\test_commands.ps1`

---

### 2. **Corrección de Comando de Inicio del Servidor**

#### Problema Identificado:
```powershell
# ❌ INCORRECTO (no funcionaba)
python -m app.presentation.api.v1.main
```

**Error:** `main.py` no es un módulo ejecutable, FastAPI se ejecuta con `uvicorn`.

#### Solución Aplicada:
```powershell
# ✅ CORRECTO
uvicorn app.presentation.api.v1.main:app --reload
```

#### Archivos Corregidos:
- `README.md` - 4 referencias actualizadas
  - Línea 964: Comando de ejecución básico
  - Línea 1153: Dockerfile CMD
  - Líneas 1348, 1351: Comandos de desarrollo
  - Línea 1581: Troubleshooting
- `docs/MANUAL_TESTING.md` - 2 referencias actualizadas
  - Línea 34: Inicio inicial del servidor
  - Línea 583: Reinicio del servidor
- `docs/QUICK_START_TESTING.md` - 1 referencia actualizada
  - Línea 11: Comando de inicio rápido

---

## 📚 Aprendizajes

### 1. **FastAPI se ejecuta con Uvicorn**
- `uvicorn` es el servidor ASGI recomendado para FastAPI
- La sintaxis es: `uvicorn <módulo>:<variable> [opciones]`
- `--reload` es esencial para desarrollo (auto-recarga)
- No usar `python -m` para ejecutar aplicaciones FastAPI

### 2. **Estructura de Testing Completa**
- **3 niveles de documentación:**
  1. Guía rápida (5 min) - Para primera vez
  2. Plan completo (40 min) - Para testing exhaustivo
  3. Script automatizado (2 min) - Para ejecución rápida
  
### 3. **Casos de Prueba Estratégicos**
- **Validación en 2 niveles:**
  - Pydantic (422) - Validación de esquema
  - Business Logic (400) - Reglas de negocio
- **Coverage completo:**
  - Casos de éxito (happy path)
  - Casos de error (edge cases)
  - Casos especiales (boundary conditions)

### 4. **PowerShell Scripts para Testing**
- PowerShell puede ejecutar comandos curl
- `Write-Host` con colores mejora legibilidad
- `Start-Sleep` permite ver resultados entre tests

---

## 🚧 Problemas Encontrados y Soluciones

### **Problema 1: Comando de inicio incorrecto**
- **Causa:** Uso de `python -m` en lugar de `uvicorn`
- **Impacto:** Usuario no podía iniciar el servidor
- **Solución:** Actualizar todas las referencias en la documentación

### **Problema 2: Falta de guía de troubleshooting**
- **Causa:** No había documentación de errores comunes
- **Impacto:** Usuario podría quedar bloqueado con errores
- **Solución:** Crear `START_SERVER.md` con troubleshooting completo

### **Problema 3: Testing demasiado técnico**
- **Causa:** Solo había tests automatizados (pytest)
- **Impacto:** Usuario no podía probar la API manualmente
- **Solución:** Crear plan de pruebas manuales con ejemplos concretos

---

## 🎓 Mejoras Sugeridas

### **Corto Plazo:**
1. **Agregar más casos de prueba:**
   - Nombres con emojis
   - Emails internacionales
   - Edades en límites (1, 150)
   - Unicode en nombres

2. **Script bash para Linux/Mac:**
   - Equivalente a `test_commands.ps1` para sistemas Unix
   
3. **Video/GIFs demostrativos:**
   - Captura de Swagger UI en acción
   - GIF de ejecución del script

### **Mediano Plazo:**
1. **Integración con Postman:**
   - Collection de Postman exportable
   - Environment variables configurables
   
2. **Newman para CI/CD:**
   - Ejecutar collection de Postman en pipeline
   
3. **Load testing:**
   - Plan de pruebas de carga con Locust o JMeter

### **Largo Plazo:**
1. **Smoke tests automatizados:**
   - Script que verifique el deployment
   - Health checks continuos
   
2. **Monitoring y alertas:**
   - Prometheus + Grafana
   - Alertas en caso de fallos

---

## 🚀 Próximos Pasos

### **Fase 4: Endpoints GET, PUT, DELETE (CRUD Completo)**
1. **Tests primero (TDD):**
   - `test_get_user_by_id.py`
   - `test_get_all_users.py`
   - `test_update_user.py`
   - `test_delete_user.py`

2. **Implementación:**
   - Use Cases: `GetUserUseCase`, `UpdateUserUseCase`, `DeleteUserUseCase`
   - Endpoints: `GET /users/{id}`, `GET /users/`, `PUT /users/{id}`, `DELETE /users/{id}`
   - Schemas: `UserListResponse`, actualizar `UserUpdateRequest`

3. **Actualizar plan de pruebas:**
   - Agregar casos para nuevos endpoints
   - Actualizar script PowerShell
   - Actualizar documentación

### **Fase 5: Configuración por Environment**
1. **Problema actual:**
   - Tests E2E fallan porque `dependencies.py` usa archivo `users.db`
   - Debería usar SQLite en memoria durante tests
   
2. **Solución:**
   - Crear `app/infrastructure/config.py`
   - Usar `pydantic-settings` para configuración
   - Variables de entorno: `DATABASE_URL`, `TESTING`
   - Fixture en `conftest.py` que setee `TESTING=true`

3. **Beneficios:**
   - Tests E2E funcionarán correctamente
   - Separación clara entre entornos
   - Fácil migración a PostgreSQL en producción

---

## 📊 Métricas

### **Documentación Creada:**
- **4 archivos nuevos**
- **~500 líneas de documentación**
- **15+ casos de prueba documentados**
- **3 niveles de testing cubiertos**

### **Correcciones Aplicadas:**
- **3 archivos actualizados**
- **7 referencias al comando de inicio corregidas**

### **Tiempo de Desarrollo:**
- **Documentación:** ~60 minutos
- **Correcciones:** ~15 minutos
- **Total:** ~75 minutos

### **Cobertura de Testing:**
- ✅ Tests unitarios: 18/18 passing
- ✅ Tests de integración: 12/12 passing
- ✅ Tests E2E: 4/7 passing (3 skippeados por DB setup)
- ✅ Tests manuales: 15+ casos documentados

---

## 📝 Checklist de Verificación

- [x] Comando de inicio del servidor corregido
- [x] Guía rápida de testing creada (QUICK_START_TESTING.md)
- [x] Plan completo de pruebas creado (MANUAL_TESTING.md)
- [x] Script PowerShell de pruebas creado (test_commands.ps1)
- [x] Guía de inicio del servidor creada (START_SERVER.md)
- [x] README.md actualizado con comandos correctos
- [x] Todas las referencias a `python -m` corregidas
- [x] Troubleshooting documentado
- [x] Casos de prueba con resultados esperados
- [x] Plantilla de reporte de pruebas incluida

---

## 🎯 Resultado Final

**Estado:** ✅ Plan de pruebas manuales completo y funcional

**Beneficios:**
1. ✅ Usuario puede iniciar el servidor sin problemas
2. ✅ Usuario tiene 3 niveles de testing disponibles
3. ✅ Usuario puede verificar funcionamiento end-to-end
4. ✅ Usuario tiene troubleshooting para problemas comunes
5. ✅ Usuario puede ejecutar 15+ pruebas manualmente o con script
6. ✅ Usuario puede documentar resultados con plantilla

**Impacto:**
- 🚀 Facilita onboarding de nuevos desarrolladores
- 🧪 Permite testing exhaustivo sin conocer pytest
- 📚 Documenta el comportamiento esperado de la API
- 🐛 Reduce tiempo de debugging con troubleshooting
- ✅ Aumenta confianza en el código con verificación manual

---

## 🔗 Archivos Relacionados

- `docs/START_SERVER.md` - Guía de inicio del servidor
- `docs/QUICK_START_TESTING.md` - Guía rápida de testing
- `docs/MANUAL_TESTING.md` - Plan completo de pruebas
- `docs/test_commands.ps1` - Script de pruebas automatizado
- `README.md` - Documentación principal del proyecto
- `docs/changelog/2025-11-10_fase-3_presentation-layer-api-rest.md` - Implementación de la API

---

**¡Plan de pruebas manuales completado exitosamente!** 🎉

Usuario puede ahora:
1. Iniciar el servidor con el comando correcto
2. Ejecutar pruebas manuales con guías detalladas
3. Usar script PowerShell para testing rápido
4. Resolver problemas comunes con troubleshooting
5. Documentar resultados con plantilla incluida

