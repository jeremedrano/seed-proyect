# Plan de Pruebas Manuales - User Management API

**Fecha:** 2025-11-10  
**Versión API:** 1.0.0  
**Objetivo:** Verificar funcionamiento end-to-end de la API REST

---

## 📋 Pre-requisitos

Antes de empezar, asegúrate de tener:

- ✅ Python 3.13.9 instalado
- ✅ Entorno virtual activado (`.venv`)
- ✅ Dependencias instaladas (`requirements.txt`)
- ✅ PowerShell o terminal abierta

---

## 🚀 Paso 1: Iniciar la Aplicación

### **1.1 Activar entorno virtual**

```powershell
cd C:\workspace\seed-proyect
.\.venv\Scripts\Activate.ps1
```

**Resultado esperado:** Verás `(.venv)` en tu prompt.

### **1.2 Iniciar servidor FastAPI**

```powershell
uvicorn app.presentation.api.v1.main:app --reload
```

**Resultado esperado:**
```
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

> ⚠️ **Nota:** Deja esta terminal abierta. La aplicación debe estar corriendo para los siguientes pasos.

---

## 🌐 Paso 2: Verificar Endpoints Básicos

### **2.1 Health Check**

**Objetivo:** Verificar que el servidor está funcionando.

**Método 1: Navegador**
```
http://localhost:8000/health
```

**Método 2: PowerShell**
```powershell
curl http://localhost:8000/health
```

**Resultado esperado:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

✅ **Test Passed** si recibes el JSON con status "healthy".

---

### **2.2 Root Endpoint**

**URL:**
```
http://localhost:8000/
```

**Resultado esperado:**
```json
{
  "message": "User Management API",
  "version": "1.0.0",
  "docs": "/api/v1/docs"
}
```

✅ **Test Passed** si recibes información de la API.

---

### **2.3 OpenAPI Documentation (Swagger UI)**

**URL:**
```
http://localhost:8000/api/v1/docs
```

**Verificar:**
- ✅ Se abre interfaz Swagger UI
- ✅ Aparece endpoint `POST /api/v1/users/`
- ✅ Puedes ver el schema de `UserCreateRequest`
- ✅ Puedes ver el schema de `UserResponse`

**Captura de pantalla recomendada:** Documenta la UI.

---

### **2.4 ReDoc Documentation**

**URL:**
```
http://localhost:8000/api/v1/redoc
```

**Verificar:**
- ✅ Se abre interfaz ReDoc
- ✅ Documentación bien formateada
- ✅ Ejemplos de request/response visibles

---

## 👤 Paso 3: Pruebas de Creación de Usuarios (POST /api/v1/users/)

### **3.1 Caso de Éxito: Crear Usuario Válido**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan.perez@example.com",
    "name": "Juan Pérez",
    "age": 30
  }'
```

**Resultado esperado:**
- **Status Code:** `201 Created`
- **Response Body:**
```json
{
  "id": 1,
  "email": "juan.perez@example.com",
  "name": "Juan Pérez",
  "age": 30
}
```

**Verificaciones:**
- ✅ Status code es 201
- ✅ Se asignó un `id` automáticamente (1, 2, 3...)
- ✅ Email, name y age coinciden con lo enviado

**En la terminal del servidor verás logs:**
```
INFO: Endpoint: POST /users/ - Creating user with email=juan.perez@example.com
INFO: Use case: CreateUser - Starting for email=juan.perez@example.com
INFO: Repository: Saving user with email=juan.perez@example.com
INFO: Repository: User saved with id=1
INFO: Endpoint: POST /users/ - User created with id=1
```

✅ **Test Passed**

---

### **3.2 Crear Más Usuarios**

**Usuario 2:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "maria.garcia@example.com",
    "name": "María García",
    "age": 25
  }'
```

**Usuario 3:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "pedro.lopez@example.com",
    "name": "Pedro López",
    "age": 35
  }'
```

**Resultado esperado:**
- Cada usuario debe recibir un ID único e incremental (1, 2, 3...)

✅ **Test Passed** si cada usuario tiene ID diferente.

---

## ❌ Paso 4: Pruebas de Validación (Casos de Error)

### **4.1 Email Duplicado**

**Objetivo:** Verificar que no se permite crear usuarios con email existente.

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan.perez@example.com",
    "name": "Otro Juan",
    "age": 40
  }'
```

**Resultado esperado:**
- **Status Code:** `400 Bad Request`
- **Response Body:**
```json
{
  "detail": "Email already exists"
}
```

**Verificaciones:**
- ✅ Status code es 400
- ✅ Mensaje indica que el email ya existe
- ✅ No se creó usuario duplicado

**En logs del servidor:**
```
WARNING: Use case: CreateUser - Email already exists: juan.perez@example.com
WARNING: Endpoint: POST /users/ - Validation error: Email already exists
```

✅ **Test Passed**

---

### **4.2 Email Inválido (Formato Incorrecto)**

**Objetivo:** Verificar validación de formato de email por Pydantic.

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "email-sin-arroba",
    "name": "Test User",
    "age": 25
  }'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Response Body:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address: ...",
      "input": "email-sin-arroba"
    }
  ]
}
```

**Verificaciones:**
- ✅ Status code es 422
- ✅ Error indica problema en campo "email"
- ✅ Pydantic rechazó el request antes de llegar al use case

✅ **Test Passed**

---

### **4.3 Edad Negativa**

**Objetivo:** Verificar validación de edad positiva.

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "age": -10
  }'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Response Body:**
```json
{
  "detail": [
    {
      "type": "greater_than",
      "loc": ["body", "age"],
      "msg": "Input should be greater than 0",
      "input": -10
    }
  ]
}
```

**Verificaciones:**
- ✅ Status code es 422
- ✅ Error indica que age debe ser > 0
- ✅ Pydantic validó correctamente

✅ **Test Passed**

---

### **4.4 Edad Cero**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "age": 0
  }'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Razón:** `gt=0` en Pydantic Field (greater than 0)

✅ **Test Passed**

---

### **4.5 Nombre Vacío**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "name": "",
    "age": 25
  }'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Razón:** `min_length=1` en Pydantic Field

✅ **Test Passed**

---

### **4.6 Campos Faltantes**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com"
  }'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Response Body:**
```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "name"],
      "msg": "Field required"
    },
    {
      "type": "missing",
      "loc": ["body", "age"],
      "msg": "Field required"
    }
  ]
}
```

**Verificaciones:**
- ✅ Status code es 422
- ✅ Errores para todos los campos faltantes
- ✅ Pydantic requiere todos los campos

✅ **Test Passed**

---

### **4.7 JSON Malformado**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{ "email": "test@example.com", "name": "Test"'
```

**Resultado esperado:**
- **Status Code:** `422 Unprocessable Entity`
- **Razón:** JSON inválido

✅ **Test Passed**

---

## 🗄️ Paso 5: Verificar Base de Datos

### **5.1 Ubicar el archivo de base de datos**

La aplicación crea un archivo SQLite:

```powershell
ls users.db
```

**Resultado esperado:**
```
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----        XX/XX/XXXX   XX:XX         XXXXX users.db
```

✅ **Test Passed** si el archivo existe.

---

### **5.2 Inspeccionar la base de datos (Opcional)**

Si tienes **DB Browser for SQLite** o similar:

1. Abrir `users.db`
2. Ir a tabla `users`
3. Ver registros:

| id | email | name | age |
|----|-------|------|-----|
| 1 | juan.perez@example.com | Juan Pérez | 30 |
| 2 | maria.garcia@example.com | María García | 25 |
| 3 | pedro.lopez@example.com | Pedro López | 35 |

**Verificar:**
- ✅ Tabla `users` existe
- ✅ Tiene columnas: id, email, name, age
- ✅ Usuarios creados están persistidos
- ✅ IDs son únicos y autoincrementales

---

### **5.3 Verificar con SQLite CLI (Alternativa)**

```powershell
# Instalar sqlite3 si no lo tienes
# choco install sqlite

sqlite3 users.db "SELECT * FROM users;"
```

**Resultado esperado:**
```
1|juan.perez@example.com|Juan Pérez|30
2|maria.garcia@example.com|María García|25
3|pedro.lopez@example.com|Pedro López|35
```

✅ **Test Passed**

---

## 🧪 Paso 6: Probar desde Swagger UI

### **6.1 Abrir Swagger UI**

```
http://localhost:8000/api/v1/docs
```

### **6.2 Crear usuario desde la interfaz**

1. **Expandir** `POST /api/v1/users/`
2. **Click** en "Try it out"
3. **Editar** el JSON de ejemplo:
```json
{
  "email": "swagger.test@example.com",
  "name": "Usuario desde Swagger",
  "age": 28
}
```
4. **Click** en "Execute"

**Resultado esperado:**
- **Response code:** `201`
- **Response body:** Usuario con ID asignado

### **6.3 Probar validación desde Swagger**

**Request con email inválido:**
```json
{
  "email": "invalid-email",
  "name": "Test",
  "age": 25
}
```

**Click** en "Execute"

**Resultado esperado:**
- **Response code:** `422`
- **Response body:** Error de validación detallado

✅ **Test Passed**

---

## 📊 Paso 7: Ejecutar Tests Automatizados

### **7.1 Abrir nueva terminal (dejar servidor corriendo)**

```powershell
cd C:\workspace\seed-proyect
.\.venv\Scripts\Activate.ps1
```

### **7.2 Ejecutar todos los tests**

```powershell
pytest tests/ -v
```

**Resultado esperado:**
```
======================== 34 passed, 3 skipped in X.XXs ========================
```

**Verificar:**
- ✅ 18 tests unitarios pasando
- ✅ 12 tests de integración pasando
- ✅ 4 tests E2E pasando
- ✅ 3 tests E2E skippeados (documentados)

### **7.3 Tests con cobertura**

```powershell
pytest tests/ --cov=app --cov-report=term-missing
```

**Resultado esperado:**
- **Coverage:** ~92%
- **Missing lines:** Muy pocas

✅ **Test Passed**

---

## 🔄 Paso 8: Reiniciar y Verificar Persistencia

### **8.1 Detener servidor**

En la terminal del servidor: `CTRL + C`

### **8.2 Reiniciar servidor**

```powershell
uvicorn app.presentation.api.v1.main:app --reload
```

### **8.3 Verificar que usuarios siguen existiendo**

**Request:**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan.perez@example.com",
    "name": "Test",
    "age": 25
  }'
```

**Resultado esperado:**
- **Status Code:** `400 Bad Request`
- **Detail:** "Email already exists"

**Verificación:**
- ✅ Los usuarios persisten después de reiniciar
- ✅ La base de datos SQLite mantiene los datos
- ✅ No se pueden crear duplicados

✅ **Test Passed**

---

## 📋 Checklist de Pruebas Completas

### **Funcionalidad Básica:**
- [ ] Servidor inicia correctamente
- [ ] Health check responde
- [ ] Root endpoint responde
- [ ] OpenAPI docs accesibles
- [ ] ReDoc accesible

### **Crear Usuarios (Casos de Éxito):**
- [ ] Crear usuario válido retorna 201
- [ ] Usuario recibe ID único
- [ ] Múltiples usuarios con IDs incrementales
- [ ] Datos se persisten en `users.db`

### **Validaciones (Casos de Error):**
- [ ] Email duplicado retorna 400
- [ ] Email inválido retorna 422
- [ ] Edad negativa retorna 422
- [ ] Edad cero retorna 422
- [ ] Nombre vacío retorna 422
- [ ] Campos faltantes retorna 422
- [ ] JSON malformado retorna 422

### **Persistencia:**
- [ ] Archivo `users.db` se crea
- [ ] Datos persisten en DB
- [ ] Datos sobreviven reinicio del servidor

### **Testing Automatizado:**
- [ ] 34 tests pasan
- [ ] 3 tests skippeados (documentados)
- [ ] Coverage > 90%

### **Swagger UI:**
- [ ] Crear usuario desde Swagger funciona
- [ ] Validaciones visibles en Swagger
- [ ] Documentación completa y clara

---

## 🎯 Resultados Esperados Finales

### **✅ Éxito Completo:**

Si todos los tests manuales pasan:

1. ✅ API REST funciona end-to-end
2. ✅ Validaciones en 2 niveles (Pydantic + Business)
3. ✅ Persistencia en SQLite funciona
4. ✅ Clean Architecture implementada correctamente
5. ✅ TDD aplicado exitosamente
6. ✅ Documentación OpenAPI generada automáticamente
7. ✅ Logging en todas las capas
8. ✅ Tests automatizados con alta cobertura

---

## 🐛 Troubleshooting

### **Problema: Puerto 8000 en uso**

**Error:**
```
ERROR: [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000)
```

**Solución:**
```powershell
# Cambiar puerto
python -c "from app.presentation.api.v1 import main; import uvicorn; uvicorn.run(main.app, port=8001)"
```

### **Problema: ModuleNotFoundError**

**Error:**
```
ModuleNotFoundError: No module named 'app'
```

**Solución:**
```powershell
# Asegúrate de estar en el directorio raíz
cd C:\workspace\seed-proyect
# Y que el venv esté activado
.\.venv\Scripts\Activate.ps1
```

### **Problema: users.db Permission Denied**

**Solución:**
```powershell
# Cerrar cualquier conexión a users.db
# Reiniciar servidor
```

---

## 📸 Capturas Recomendadas

Para documentar las pruebas, toma capturas de:

1. ✅ Swagger UI mostrando el endpoint
2. ✅ Request exitoso con 201
3. ✅ Error de validación 422
4. ✅ Error de negocio 400
5. ✅ Tabla users en DB con registros
6. ✅ Logs del servidor en consola
7. ✅ Tests pasando con pytest

---

## ⏱️ Tiempo Estimado

- **Setup inicial:** 5 minutos
- **Pruebas de éxito:** 10 minutos
- **Pruebas de validación:** 15 minutos
- **Verificación de DB:** 5 minutos
- **Tests automatizados:** 5 minutos
- **Total:** ~40 minutos

---

## 📝 Plantilla de Reporte de Pruebas

```markdown
# Reporte de Pruebas Manuales

**Fecha:** YYYY-MM-DD
**Ejecutado por:** [Tu nombre]
**Versión API:** 1.0.0

## Resultados:

| Test | Resultado | Notas |
|------|-----------|-------|
| Health Check | ✅ / ❌ | |
| Crear usuario válido | ✅ / ❌ | |
| Email duplicado | ✅ / ❌ | |
| Email inválido | ✅ / ❌ | |
| Edad negativa | ✅ / ❌ | |
| Nombre vacío | ✅ / ❌ | |
| Persistencia DB | ✅ / ❌ | |
| Tests automatizados | ✅ / ❌ | XX/37 passing |

## Observaciones:

[Cualquier nota adicional]

## Conclusión:

[ ] Todas las pruebas pasaron
[ ] Algunas pruebas fallaron (detallar)
```

---

**¡Buena suerte con las pruebas!** 🚀

Si encuentras algún problema, revisa la sección de Troubleshooting o consulta los logs del servidor.

