# 🚀 Quick Start - Testing Guide

## Inicio Rápido en 3 Pasos

### **Paso 1: Iniciar el Servidor** ⚡

```powershell
# En PowerShell
cd C:\workspace\seed-proyect
.\.venv\Scripts\Activate.ps1
uvicorn app.presentation.api.v1.main:app --reload
```

**✅ Servidor corriendo en:** `http://localhost:8000`

> 💡 **¿Problemas para iniciar?** Ver guía detallada: `docs/START_SERVER.md`

---

### **Paso 2: Abrir Swagger UI** 🌐

Abre tu navegador en:
```
http://localhost:8000/api/v1/docs
```

**Prueba crear un usuario:**
1. Click en `POST /api/v1/users/`
2. Click en "Try it out"
3. Modifica el JSON:
```json
{
  "email": "test@example.com",
  "name": "Test User",
  "age": 25
}
```
4. Click en "Execute"

**✅ Deberías ver:** Status 201 con el usuario creado

---

### **Paso 3: Ejecutar Script de Pruebas** 🧪

**Opción A: Ejecutar el script completo**
```powershell
# En otra terminal (dejar servidor corriendo)
cd C:\workspace\seed-proyect
.\docs\test_commands.ps1
```

**Opción B: Ejecutar comandos manualmente**

Sigue el archivo: `docs/MANUAL_TESTING.md`

**Opción C: Ejecutar tests automatizados**
```powershell
pytest tests/ -v
```

**✅ Resultado esperado:** 34 passed, 3 skipped

---

## 📋 Archivos de Pruebas Disponibles

| Archivo | Descripción | Uso |
|---------|-------------|-----|
| `docs/MANUAL_TESTING.md` | Plan completo de pruebas manuales | Guía detallada paso a paso |
| `docs/test_commands.ps1` | Script con comandos curl | Ejecutar pruebas automáticas |
| `docs/QUICK_START_TESTING.md` | Esta guía | Inicio rápido |

---

## 🎯 Casos de Prueba Rápidos

### ✅ **Crear Usuario Exitoso**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{"email":"test@example.com","name":"Test","age":25}'
```
**Esperar:** 201 Created

---

### ❌ **Email Duplicado**
```powershell
# Ejecutar el mismo comando de arriba dos veces
```
**Esperar:** 400 Bad Request

---

### ❌ **Email Inválido**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{"email":"invalid-email","name":"Test","age":25}'
```
**Esperar:** 422 Unprocessable Entity

---

### ❌ **Edad Negativa**
```powershell
curl -X POST http://localhost:8000/api/v1/users/ `
  -H "Content-Type: application/json" `
  -d '{"email":"test2@example.com","name":"Test","age":-5}'
```
**Esperar:** 422 Unprocessable Entity

---

## 🔍 Verificar Base de Datos

```powershell
# Ver si existe users.db
ls users.db

# Si tienes sqlite3 instalado
sqlite3 users.db "SELECT * FROM users;"
```

---

## 🧪 Ejecutar Tests Automatizados

### **Todos los tests**
```powershell
pytest tests/ -v
```

### **Solo tests unitarios**
```powershell
pytest tests/unit/ -v
```

### **Solo tests de integración**
```powershell
pytest tests/integration/ -v
```

### **Solo tests E2E**
```powershell
pytest tests/e2e/ -v
```

### **Con cobertura**
```powershell
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 📊 Resultados Esperados

### **✅ Tests Automatizados:**
```
======================== 34 passed, 3 skipped in 0.71s ========================
```

### **✅ Cobertura:**
```
TOTAL: 95% coverage
```

### **✅ Servidor:**
- Health check: `http://localhost:8000/health` → 200 OK
- Docs: `http://localhost:8000/api/v1/docs` → Swagger UI
- API funcionando correctamente

---

## 🐛 Troubleshooting Rápido

### **Problema: Puerto en uso**
```powershell
# Cerrar otros procesos en puerto 8000
netstat -ano | findstr :8000
```

### **Problema: ModuleNotFoundError**
```powershell
# Verificar que estás en el directorio correcto
cd C:\workspace\seed-proyect
# Y que el venv está activado
.\.venv\Scripts\Activate.ps1
```

### **Problema: Tests fallan**
```powershell
# Actualizar dependencias
uv pip install -r requirements.txt
```

---

## 📝 Checklist Rápido

- [ ] Servidor inicia sin errores
- [ ] `/health` retorna 200
- [ ] Swagger UI accesible
- [ ] Crear usuario retorna 201
- [ ] Email duplicado retorna 400
- [ ] Validaciones Pydantic retornan 422
- [ ] `users.db` existe
- [ ] Tests automatizados pasan (34/37)

---

## ⏱️ Tiempo Estimado

- **Setup:** 2 minutos
- **Pruebas básicas:** 5 minutos  
- **Pruebas completas:** 15 minutos
- **Total:** ~20 minutos

---

## 🎓 Siguiente Nivel

Una vez que todo funcione:

1. **Explorar Swagger UI** - Probar diferentes combinaciones
2. **Ver logs del servidor** - Entender el flujo de requests
3. **Inspeccionar users.db** - Ver cómo se almacenan los datos
4. **Leer el código** - Entender Clean Architecture
5. **Agregar más features** - GET, PUT, DELETE endpoints

---

## 📚 Documentación Adicional

- **Plan completo:** `docs/MANUAL_TESTING.md`
- **Changelogs:** `docs/changelog/`
- **README principal:** `README.md`
- **Cursor rules:** `.cursorrules`

---

**¡Happy Testing!** 🚀

Si todo funciona correctamente, habrás verificado que:
- ✅ Clean Architecture está implementada
- ✅ TDD fue aplicado correctamente
- ✅ API REST funciona end-to-end
- ✅ Validaciones en múltiples niveles funcionan
- ✅ Persistencia en SQLite funciona

