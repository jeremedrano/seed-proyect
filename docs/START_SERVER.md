# 🚀 Cómo Iniciar el Servidor

## Comando Correcto ✅

```powershell
cd C:\workspace\seed-proyect
.\.venv\Scripts\Activate.ps1
uvicorn app.presentation.api.v1.main:app --reload
```

---

## Explicación del Comando

```powershell
uvicorn app.presentation.api.v1.main:app --reload
```

- `uvicorn` - Servidor ASGI para FastAPI
- `app.presentation.api.v1.main:app` - Ruta completa al objeto `app` de FastAPI
  - `app.presentation.api.v1.main` - Módulo Python (archivo main.py)
  - `:app` - Variable dentro de main.py que contiene la aplicación FastAPI
- `--reload` - Auto-recarga cuando cambias código (solo para desarrollo)

---

## Salida Esperada ✅

Cuando el servidor inicia correctamente verás:

```
INFO:     Will watch for changes in these directories: ['C:\\workspace\\seed-proyect']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using WatchFiles
INFO:     Started server process [YYYY]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Verificar que Funciona

### 1. Abrir navegador:

**Health Check:**
```
http://localhost:8000/health
```

**Documentación Swagger:**
```
http://localhost:8000/api/v1/docs
```

**API Root:**
```
http://localhost:8000/
```

---

### 2. Desde PowerShell:

```powershell
curl http://localhost:8000/health
```

**Respuesta esperada:**
```json
{
  "status": "ok",
  "message": "API is running"
}
```

---

## Detener el Servidor

Presiona: `CTRL + C`

Verás:
```
INFO:     Shutting down
INFO:     Finished server process [YYYY]
INFO:     Stopping reloader process [XXXX]
```

---

## Opciones Adicionales

### **Cambiar puerto:**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --port 8001
```

### **Cambiar host (accesible desde red):**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --host 0.0.0.0
```

### **Sin auto-reload (producción):**
```powershell
uvicorn app.presentation.api.v1.main:app
```

### **Con más workers (producción):**
```powershell
uvicorn app.presentation.api.v1.main:app --workers 4
```

⚠️ **Nota:** `--reload` y `--workers` no se pueden usar juntos.

---

## Troubleshooting

### ❌ Error: "No module named 'app'"

**Causa:** No estás en el directorio correcto.

**Solución:**
```powershell
cd C:\workspace\seed-proyect
pwd  # Verificar que estás en el directorio correcto
```

---

### ❌ Error: "Address already in use"

**Causa:** El puerto 8000 ya está en uso por otro proceso.

**Solución 1 - Usar otro puerto:**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --port 8001
```

**Solución 2 - Encontrar y cerrar el proceso:**
```powershell
# Ver qué proceso usa el puerto 8000
netstat -ano | findstr :8000

# Cerrar el proceso (reemplazar PID con el número que obtuviste)
taskkill /PID <PID> /F
```

---

### ❌ Error: "uvicorn: command not found"

**Causa:** El entorno virtual no está activado o uvicorn no está instalado.

**Solución:**
```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Verificar que uvicorn esté instalado
uv pip list | findstr uvicorn

# Si no está, instalarlo
uv pip install uvicorn[standard]
```

---

### ❌ Error: "Failed to import 'app' from 'app.presentation.api.v1.main'"

**Causa:** Error en el código de main.py o dependencias faltantes.

**Solución:**
```powershell
# Verificar que todas las dependencias estén instaladas
uv pip install -r requirements.txt

# Ver el error completo para más detalles
uvicorn app.presentation.api.v1.main:app --log-level debug
```

---

## Logs del Servidor

### **Ver logs en tiempo real:**

El servidor muestra logs automáticamente en la consola.

Ejemplo de logs:
```
INFO:     127.0.0.1:XXXXX - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:XXXXX - "POST /api/v1/users/ HTTP/1.1" 201 Created
INFO:     127.0.0.1:XXXXX - "GET /api/v1/docs HTTP/1.1" 200 OK
```

### **Aumentar nivel de logging:**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --log-level debug
```

Niveles disponibles:
- `critical` - Solo errores críticos
- `error` - Errores
- `warning` - Advertencias (default)
- `info` - Información general
- `debug` - Debug detallado
- `trace` - Traza completa (muy verboso)

---

## Comandos Rápidos de Referencia

### **Desarrollo (recomendado):**
```powershell
uvicorn app.presentation.api.v1.main:app --reload
```

### **Desarrollo con puerto personalizado:**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --port 8001
```

### **Desarrollo accesible desde red:**
```powershell
uvicorn app.presentation.api.v1.main:app --reload --host 0.0.0.0
```

### **Producción (sin auto-reload):**
```powershell
uvicorn app.presentation.api.v1.main:app --host 0.0.0.0 --port 8000
```

---

## URLs Útiles

Una vez que el servidor está corriendo:

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000/` | Root endpoint - Info de la API |
| `http://localhost:8000/health` | Health check |
| `http://localhost:8000/api/v1/docs` | Swagger UI (documentación interactiva) |
| `http://localhost:8000/api/v1/redoc` | ReDoc (documentación alternativa) |
| `http://localhost:8000/api/v1/openapi.json` | Esquema OpenAPI en JSON |

---

## Siguiente Paso

Una vez que el servidor esté corriendo:

1. **Abre Swagger UI:** `http://localhost:8000/api/v1/docs`
2. **Sigue la guía rápida:** `docs/QUICK_START_TESTING.md`
3. **O ejecuta el script de pruebas:** `docs/test_commands.ps1`

---

**¡Listo para empezar!** 🎉

