# Plan de Trabajo: Sistema de Gestión de Usuarios con FastAPI y UV

## 📋 Descripción del Proyecto
Desarrollo de una API REST para **gestión de usuarios** con operaciones CRUD, **autenticación segura (JWT)**, hashing de contraseñas con bcrypt, utilizando FastAPI, gestión de dependencias con UV, ejecución en entorno virtual (VENV) y preparación para contenerización con Docker.

---

## 🎯 Objetivos del Proyecto

1. Implementar un CRUD completo de usuarios con FastAPI
2. Implementar sistema de autenticación seguro con JWT
3. Proteger contraseñas con bcrypt/passlib
4. Configurar gestión de dependencias con UV
5. Ejecutar en entorno virtual (VENV)
6. Implementar autorización basada en roles
7. Preparar infraestructura para contenerización (Docker)

---

## 📐 Arquitectura Propuesta

```
seed-proyect/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la aplicación
│   ├── config.py                # Configuraciones
│   ├── database.py              # Configuración de base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py              # Modelo de Usuario (SQLAlchemy)
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py              # Schemas de Usuario (Pydantic)
│   │   └── auth.py              # Schemas de Autenticación (Login, Token)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── users.py             # Endpoints CRUD de usuarios
│   │   └── auth.py              # Endpoints de autenticación (login, register)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py      # Lógica de negocio de usuarios
│   │   └── auth_service.py      # Lógica de autenticación
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py          # Funciones de seguridad (hash, JWT)
│   │   └── dependencies.py      # Dependencias de autenticación
│   └── utils/
│       ├── __init__.py
│       └── logger.py            # Configuración de logging
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_auth.py
├── .env                         # Variables de entorno
├── .gitignore
├── pyproject.toml               # Configuración UV
├── README.md
└── requirements.txt             # Dependencias del proyecto
```

---

## 🗓️ Plan de Trabajo Detallado

### **FASE 1: Configuración del Entorno de Desarrollo**

#### 1.1 Instalación de UV
**Objetivo:** Instalar el gestor de paquetes UV

**Comandos:**
```powershell
# Instalación de UV (Windows PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verificación:**
```powershell
uv --version
```

#### 1.2 Creación del Entorno Virtual
**Objetivo:** Configurar un entorno virtual aislado para el proyecto

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Crear entorno virtual con UV
uv venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1
```

**Resultado Esperado:**
- Directorio `.venv/` creado
- Prompt debe mostrar `(.venv)` al inicio

#### 1.3 Instalación de Dependencias Base
**Objetivo:** Instalar FastAPI y dependencias principales

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Con entorno virtual activado
uv pip install fastapi[all]
uv pip install uvicorn[standard]
uv pip install sqlalchemy
uv pip install python-dotenv
uv pip install pydantic
uv pip install pydantic-settings
```

#### 1.4 Instalación de Dependencias de Seguridad
**Objetivo:** Instalar librerías para autenticación y seguridad

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Dependencias de seguridad
uv pip install "passlib[bcrypt]"
uv pip install python-jose[cryptography]
uv pip install python-multipart
```

**Justificación:**
- `passlib[bcrypt]`: Hashing seguro de contraseñas con bcrypt
- `python-jose[cryptography]`: Creación y validación de tokens JWT
- `python-multipart`: Soporte para formularios (login con form-data)

#### 1.5 Generar archivo de dependencias
**Objetivo:** Documentar dependencias del proyecto

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
uv pip freeze > requirements.txt
```

---

### **FASE 2: Estructura Base del Proyecto**

#### 2.1 Crear Estructura de Directorios
**Objetivo:** Organizar el proyecto siguiendo mejores prácticas

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
New-Item -ItemType Directory -Path app, app\models, app\schemas, app\routes, app\services, app\core, app\utils, tests -Force
```

#### 2.2 Crear Archivos __init__.py
**Objetivo:** Convertir directorios en paquetes Python

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
New-Item -ItemType File -Path app\__init__.py, app\models\__init__.py, app\schemas\__init__.py, app\routes\__init__.py, app\services\__init__.py, app\core\__init__.py, app\utils\__init__.py, tests\__init__.py
```

#### 2.3 Crear archivo .gitignore
**Objetivo:** Excluir archivos innecesarios del control de versiones

**Contenido sugerido:**
```
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
.DS_Store
```

---

### **FASE 3: Configuración de Base de Datos**

#### 3.1 Decidir Base de Datos
**Opciones:**
- **SQLite:** Ideal para desarrollo y pruebas (sin instalación adicional)
- **PostgreSQL:** Recomendado para producción

**Para SQLite (recomendado inicialmente):**
- No requiere instalación adicional
- Archivo de base de datos: `app.db`

**Para PostgreSQL:**
```powershell
uv pip install psycopg2-binary
```

#### 3.2 Crear archivo de configuración (.env)
**Objetivo:** Centralizar variables de entorno

**Contenido de `.env`:**
```env
# Base de datos
DATABASE_URL=sqlite:///./app.db

# Configuración general
API_VERSION=v1
DEBUG=True

# Seguridad JWT
SECRET_KEY=tu_clave_secreta_super_segura_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Generar SECRET_KEY seguro:**
```powershell
# Desde PowerShell con Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**⚠️ IMPORTANTE:** Nunca commitear el archivo `.env` con claves reales al repositorio

#### 3.3 Implementar database.py
**Objetivo:** Configurar conexión a base de datos con SQLAlchemy

**Archivo:** `app/database.py`
**Componentes:**
- Engine de SQLAlchemy
- SessionLocal
- Base declarativa
- Dependency para obtener sesión DB

---

### **FASE 4: Implementación de Seguridad y Autenticación**

#### 4.1 Implementar Funciones de Seguridad
**Objetivo:** Crear funciones para hashing de contraseñas y JWT

**Archivo:** `app/core/security.py`
**Funciones necesarias:**
- `get_password_hash(password)`: Hash de contraseña con bcrypt
- `verify_password(plain_password, hashed_password)`: Verificar contraseña
- `create_access_token(data, expires_delta)`: Crear token JWT
- `create_refresh_token(data, expires_delta)`: Crear token de refresco

**Características:**
- Usar `passlib.context.CryptContext` con bcrypt
- Usar `jose.jwt` para tokens JWT
- Configurar tiempo de expiración desde settings
- Logging de operaciones de seguridad

#### 4.2 Implementar Dependencias de Autenticación
**Objetivo:** Crear dependencias para proteger endpoints

**Archivo:** `app/core/dependencies.py`
**Funciones necesarias:**
- `get_current_user(token: str)`: Obtener usuario desde token JWT
- `get_current_active_user(current_user)`: Verificar que usuario esté activo
- `require_role(roles: list)`: Dependency para verificar roles

**Características:**
- Validar token JWT
- Extraer información del usuario
- Manejar tokens expirados o inválidos
- Verificar permisos por rol

---

### **FASE 5: Implementación del Modelo de Usuario**

#### 5.1 Definir Modelo SQLAlchemy de Usuario
**Objetivo:** Crear modelo de base de datos para usuarios

**Archivo:** `app/models/user.py`
**Componentes:**
- Clase User heredando de Base
- Campos principales:
  - `id`: Integer, Primary Key
  - `email`: String(255), Unique, Index
  - `username`: String(100), Unique, Index
  - `full_name`: String(255)
  - `hashed_password`: String(255)
  - `is_active`: Boolean, default=True
  - `is_superuser`: Boolean, default=False
  - `role`: String(50), default="user" (user, admin, superadmin)
  - `created_at`: DateTime
  - `updated_at`: DateTime
  - `last_login`: DateTime, nullable
- Índices y constraints
- Método `__repr__` para debugging

**Validaciones:**
- Email único y válido
- Username único
- Password nunca se almacena en texto plano

#### 5.2 Definir Schemas Pydantic de Usuario
**Objetivo:** Validar datos de entrada/salida de usuarios

**Archivo:** `app/schemas/user.py`
**Schemas necesarios:**
- `UserBase`: Campos comunes (email, username, full_name)
- `UserCreate`: Datos para registro (incluye password sin hash)
- `UserUpdate`: Datos para actualización (campos opcionales)
- `UserInDB`: Usuario con hashed_password (solo para uso interno)
- `UserResponse`: Respuesta pública (sin password)
- Configuración de `from_attributes = True` (orm_mode en Pydantic v2)

**Validaciones:**
- Email con formato válido
- Username: 3-50 caracteres, alfanumérico
- Password: mínimo 8 caracteres, al menos 1 mayúscula, 1 minúscula, 1 número
- Full name: 1-255 caracteres

#### 5.3 Definir Schemas de Autenticación
**Objetivo:** Validar datos de login y tokens

**Archivo:** `app/schemas/auth.py`
**Schemas necesarios:**
- `LoginRequest`: Credenciales de login (email/username, password)
- `TokenResponse`: Respuesta con tokens (access_token, refresh_token, token_type)
- `TokenData`: Datos extraídos del token (user_id, email, role)
- `RefreshTokenRequest`: Request para renovar token

---

### **FASE 6: Implementación de Servicios de Negocio**

#### 6.1 Crear Servicio de Autenticación
**Objetivo:** Implementar lógica de autenticación

**Archivo:** `app/services/auth_service.py`
**Funciones:**
- `authenticate_user(db, email_or_username, password)`: Autenticar usuario
- `register_user(db, user_data)`: Registrar nuevo usuario
- `login(db, credentials)`: Procesar login y generar tokens
- `refresh_access_token(db, refresh_token)`: Renovar token de acceso
- `logout(db, user_id)`: Logout (opcional, invalidar tokens)

**Características:**
- Verificar contraseñas con bcrypt
- Generar tokens JWT
- Validar que usuario esté activo
- Actualizar last_login
- Logging exhaustivo de intentos de login (exitosos y fallidos)
- Manejo de errores específicos (credenciales inválidas, usuario inactivo)

#### 6.2 Crear Servicio CRUD de Usuarios
**Objetivo:** Implementar operaciones CRUD para gestión de usuarios

**Archivo:** `app/services/user_service.py`
**Funciones:**
- `create_user(db, user_data)`: Crear nuevo usuario (hash password)
- `get_user_by_id(db, user_id)`: Obtener usuario por ID
- `get_user_by_email(db, email)`: Obtener usuario por email
- `get_user_by_username(db, username)`: Obtener usuario por username
- `get_users(db, skip, limit, filters)`: Listar usuarios con paginación
- `update_user(db, user_id, user_data)`: Actualizar usuario
- `update_password(db, user_id, old_password, new_password)`: Cambiar contraseña
- `delete_user(db, user_id)`: Eliminar usuario (soft delete recomendado)
- `activate_user(db, user_id)`: Activar usuario
- `deactivate_user(db, user_id)`: Desactivar usuario

**Características:**
- Hash de contraseñas antes de guardar
- Validar que email/username no estén duplicados
- No permitir actualizar campos sensibles directamente
- Logging exhaustivo para debugging y auditoría
- Validaciones de negocio (ej: no eliminar superadmin)

---

### **FASE 7: Implementación de Endpoints**

#### 7.1 Crear Router de Autenticación
**Objetivo:** Definir endpoints públicos de autenticación

**Archivo:** `app/routes/auth.py`
**Endpoints:**
- `POST /auth/register`: Registro de nuevo usuario
- `POST /auth/login`: Login (retorna access_token y refresh_token)
- `POST /auth/refresh`: Renovar access token con refresh token
- `POST /auth/logout`: Logout (opcional)
- `GET /auth/me`: Obtener información del usuario actual (protegido)

**Características:**
- Endpoints públicos (register, login, refresh)
- Endpoint protegido (me) requiere JWT válido
- Decoradores OpenAPI completos
- Validaciones con Pydantic
- Status codes apropiados:
  - 200: Login exitoso
  - 201: Usuario registrado
  - 400: Datos inválidos
  - 401: No autenticado o credenciales inválidas
  - 409: Email/username ya existe
- Logging exhaustivo de operaciones de autenticación

#### 7.2 Crear Router CRUD de Usuarios
**Objetivo:** Definir endpoints REST para gestión de usuarios (protegidos)

**Archivo:** `app/routes/users.py`
**Endpoints:**
- `POST /users/`: Crear usuario (admin only)
- `GET /users/`: Listar usuarios con paginación (admin only)
- `GET /users/{user_id}`: Obtener usuario específico (propio o admin)
- `GET /users/me`: Obtener perfil propio (protegido)
- `PUT /users/{user_id}`: Actualizar usuario completo (propio o admin)
- `PATCH /users/{user_id}`: Actualizar usuario parcialmente (propio o admin)
- `PATCH /users/{user_id}/password`: Cambiar contraseña (propio)
- `DELETE /users/{user_id}`: Eliminar usuario (admin only)
- `PATCH /users/{user_id}/activate`: Activar usuario (admin only)
- `PATCH /users/{user_id}/deactivate`: Desactivar usuario (admin only)

**Características:**
- Todos los endpoints protegidos con JWT
- Autorización basada en roles (user, admin, superadmin)
- Usuario puede ver/editar su propio perfil
- Admin puede gestionar todos los usuarios
- Decoradores OpenAPI (@Operation, @ApiResponses)
- Validaciones con Pydantic
- Status codes HTTP apropiados
- Manejo de errores con HTTPException
- Logging en cada endpoint

---

### **FASE 8: Configuración de la Aplicación Principal**

#### 8.1 Implementar config.py
**Objetivo:** Centralizar configuraciones

**Archivo:** `app/config.py`
**Componentes:**
- Clase Settings con pydantic-settings
- Carga de variables de entorno desde .env
- Configuraciones por ambiente (dev/prod)
- Variables de seguridad (SECRET_KEY, ALGORITHM, etc.)
- Configuración de base de datos
- Configuración de CORS

**Campos de Settings:**
- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES
- REFRESH_TOKEN_EXPIRE_DAYS
- API_VERSION
- DEBUG
- ALLOWED_ORIGINS (para CORS)

#### 8.2 Implementar main.py
**Objetivo:** Configurar y arrancar la aplicación FastAPI

**Archivo:** `app/main.py`
**Componentes:**
- Instancia de FastAPI con metadata
- Configuración de CORS (permitir orígenes específicos)
- Registro de routers:
  - `/auth` (autenticación - público)
  - `/users` (gestión de usuarios - protegido)
- Event handlers:
  - `startup`: Crear tablas en base de datos, crear usuario admin inicial
  - `shutdown`: Cerrar conexiones
- Middleware de logging para cada request
- Configuración de documentación OpenAPI/Swagger
- Exception handlers personalizados

**Características:**
- Título y descripción de API
- Versión de API
- Tags organizados (Auth, Users)
- Crear superadmin inicial si no existe

---

### **FASE 9: Testing**

#### 9.1 Instalar Dependencias de Testing
**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
uv pip install pytest
uv pip install httpx
uv pip install pytest-cov
uv pip install pytest-asyncio
```

#### 9.2 Implementar Tests de Autenticación
**Archivo:** `tests/test_auth.py`
**Tests necesarios:**
- `test_register_user`: Registro exitoso de usuario
- `test_register_duplicate_email`: Error al registrar email duplicado
- `test_register_duplicate_username`: Error al registrar username duplicado
- `test_register_invalid_password`: Error con contraseña débil
- `test_login_success`: Login exitoso con credenciales válidas
- `test_login_invalid_credentials`: Error con credenciales inválidas
- `test_login_inactive_user`: Error al intentar login con usuario inactivo
- `test_refresh_token`: Renovar access token con refresh token válido
- `test_refresh_token_invalid`: Error con refresh token inválido
- `test_get_current_user`: Obtener usuario actual con token válido

#### 9.3 Implementar Tests CRUD de Usuarios
**Archivo:** `tests/test_users.py`
**Tests necesarios:**
- `test_create_user_as_admin`: Admin crea usuario
- `test_create_user_as_user`: Usuario normal no puede crear usuarios
- `test_get_users_as_admin`: Admin lista todos los usuarios con paginación
- `test_get_users_as_user`: Usuario normal no puede listar usuarios
- `test_get_own_profile`: Usuario obtiene su propio perfil
- `test_get_user_by_id_as_admin`: Admin obtiene usuario por ID
- `test_update_own_profile`: Usuario actualiza su propio perfil
- `test_update_other_user_as_user`: Usuario no puede actualizar otros usuarios
- `test_update_user_as_admin`: Admin actualiza cualquier usuario
- `test_change_password`: Usuario cambia su contraseña
- `test_change_password_wrong_old`: Error con contraseña antigua incorrecta
- `test_delete_user_as_admin`: Admin elimina usuario
- `test_delete_user_as_user`: Usuario no puede eliminar usuarios
- `test_activate_deactivate_user`: Admin activa/desactiva usuario

#### 9.4 Ejecutar Tests
**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest tests/ --cov=app --cov-report=html

# Ejecutar solo tests de autenticación
pytest tests/test_auth.py -v

# Ejecutar solo tests de usuarios
pytest tests/test_users.py -v
```

---

### **FASE 10: Ejecución y Verificación**

#### 10.1 Ejecutar la Aplicación
**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Asegurarse de que el VENV esté activado
.\.venv\Scripts\Activate.ps1

# Ejecutar con uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Resultado Esperado:**
- Servidor corriendo en `http://localhost:8000`
- Documentación interactiva en `http://localhost:8000/docs`
- Documentación alternativa en `http://localhost:8000/redoc`
- Usuario superadmin creado automáticamente en primer arranque
- Logs mostrando inicio correcto de la aplicación

#### 10.2 Verificar Endpoints con Swagger UI
**Usando la documentación interactiva:**
1. Acceder a `http://localhost:8000/docs`
2. **Probar Registro:**
   - Endpoint: `POST /auth/register`
   - Crear usuario de prueba
3. **Probar Login:**
   - Endpoint: `POST /auth/login`
   - Obtener access_token
4. **Autorizar en Swagger:**
   - Click en "Authorize" (candado verde)
   - Ingresar: `Bearer {tu_access_token}`
5. **Probar Endpoints Protegidos:**
   - `GET /auth/me`: Ver perfil actual
   - `GET /users/me`: Ver perfil propio
   - `PATCH /users/{id}/password`: Cambiar contraseña
   - `GET /users/`: Listar usuarios (solo admin)

#### 10.3 Verificar Endpoints con PowerShell
**Desde:** `C:\workspace\seed-proyect`

**1. Registrar nuevo usuario:**
```powershell
$registerBody = @{
    email = "usuario@ejemplo.com"
    username = "usuario_test"
    full_name = "Usuario de Prueba"
    password = "Password123!"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/register" -ContentType "application/json" -Body $registerBody
```

**2. Login:**
```powershell
$loginBody = @{
    email = "usuario@ejemplo.com"
    password = "Password123!"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/login" -ContentType "application/json" -Body $loginBody

# Guardar token en variable
$token = $loginResponse.access_token
Write-Host "Token obtenido: $token"
```

**3. Obtener perfil actual (con token):**
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
}

Invoke-RestMethod -Method Get -Uri "http://localhost:8000/auth/me" -Headers $headers
```

**4. Actualizar perfil propio:**
```powershell
$updateBody = @{
    full_name = "Nuevo Nombre Completo"
} | ConvertTo-Json

Invoke-RestMethod -Method Patch -Uri "http://localhost:8000/users/me" -Headers $headers -ContentType "application/json" -Body $updateBody
```

**5. Cambiar contraseña:**
```powershell
$passwordBody = @{
    old_password = "Password123!"
    new_password = "NewPassword456!"
} | ConvertTo-Json

Invoke-RestMethod -Method Patch -Uri "http://localhost:8000/users/me/password" -Headers $headers -ContentType "application/json" -Body $passwordBody
```

**6. Listar usuarios (requiere admin):**
```powershell
# Primero login como admin
$adminLoginBody = @{
    email = "admin@ejemplo.com"
    password = "AdminPassword123!"
} | ConvertTo-Json

$adminResponse = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/login" -ContentType "application/json" -Body $adminLoginBody
$adminToken = $adminResponse.access_token

$adminHeaders = @{
    "Authorization" = "Bearer $adminToken"
}

# Listar usuarios
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/users/?skip=0&limit=10" -Headers $adminHeaders
```

---

### **FASE 11: Documentación y Mejoras de Seguridad**

#### 11.1 Documentar API
**Objetivo:** Mejorar documentación OpenAPI

**Tareas:**
- Agregar descripciones detalladas a todos los endpoints
- Documentar modelos de request/response con ejemplos
- Agregar ejemplos de tokens JWT en documentación
- Configurar tags para organizar endpoints (Auth, Users)
- Documentar códigos de error posibles
- Agregar descripción de flujo de autenticación

#### 11.2 Implementar Validaciones Adicionales
**Mejoras sugeridas:**
- Validación avanzada de contraseñas (mayúsculas, números, caracteres especiales)
- Validación de formato de email con regex
- Límites en longitud de strings (username 3-50 caracteres)
- Custom validators en Pydantic para reglas de negocio
- Validación de roles permitidos
- Sanitización de inputs para prevenir inyecciones

#### 11.3 Mejoras de Seguridad
**Implementaciones recomendadas:**
- **Rate Limiting:** Limitar intentos de login (ej: 5 intentos cada 15 minutos)
- **Token Blacklist:** Lista negra para tokens revocados (logout)
- **Password History:** No permitir reutilizar últimas 3 contraseñas
- **Email Verification:** Verificar email con token de activación
- **Two-Factor Authentication (2FA):** Autenticación de dos factores
- **Audit Log:** Registrar todas las operaciones sensibles
- **HTTPS Only:** Forzar conexiones seguras en producción
- **CORS Configurado:** Permitir solo orígenes específicos

#### 11.4 Implementar Manejo de Errores Avanzado
**Mejoras:**
- Exception handlers personalizados para cada tipo de error
- Respuestas de error estandarizadas con formato JSON consistente
- Logging estructurado con niveles apropiados
- Códigos de error específicos para diferentes casos
- No exponer información sensible en errores
- Stack traces solo en modo DEBUG

---

### **FASE 12: Preparación para Contenerización (Docker)**

#### 12.1 Crear Dockerfile
**Objetivo:** Definir imagen Docker para la aplicación

**Archivo:** `Dockerfile`
**Contenido sugerido:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY ./app ./app

# Crear usuario no-root por seguridad
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/docs')"

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 12.2 Crear docker-compose.yml
**Objetivo:** Orquestar servicios (API + Base de datos)

**Archivo:** `docker-compose.yml`
**Contenido sugerido:**
```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: fastapi-users-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/usersdb
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
    depends_on:
      - db
    volumes:
      - ./app:/app/app
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=usersdb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@ejemplo.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - db
    restart: unless-stopped

volumes:
  postgres_data:
```

#### 12.3 Crear .dockerignore
**Objetivo:** Excluir archivos innecesarios de la imagen

**Contenido:**
```
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.gitignore
.env
.env.*
tests/
*.md
.pytest_cache/
htmlcov/
.coverage
*.db
*.sqlite
```

#### 12.4 Crear .env.docker (ejemplo)
**Objetivo:** Variables de entorno para Docker

**Archivo:** `.env.docker`
```env
DATABASE_URL=postgresql://user:password@db:5432/usersdb
SECRET_KEY=generar_con_secrets.token_urlsafe
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
API_VERSION=v1
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

#### 12.5 Probar Contenerización
**Comandos desde:** `C:\workspace\seed-proyect`

**Construir y ejecutar con Docker:**
```powershell
# Construir imagen
docker build -t fastapi-users-api .

# Ejecutar contenedor con SQLite
docker run -d -p 8000:8000 --name fastapi-app -e DATABASE_URL=sqlite:///./app.db fastapi-users-api

# Verificar logs
docker logs fastapi-app

# Verificar que funciona
Invoke-RestMethod -Method Get -Uri "http://localhost:8000/docs"

# Detener y eliminar contenedor
docker stop fastapi-app
docker rm fastapi-app
```

**Con docker-compose (recomendado):**
```powershell
# Levantar todos los servicios (API + PostgreSQL + pgAdmin)
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs solo de la API
docker-compose logs -f api

# Ver estado de servicios
docker-compose ps

# Ejecutar migraciones (si usas Alembic)
docker-compose exec api alembic upgrade head

# Crear usuario admin inicial
docker-compose exec api python -c "from app.database import SessionLocal; from app.services.user_service import create_user; from app.schemas.user import UserCreate; db = SessionLocal(); create_user(db, UserCreate(email='admin@ejemplo.com', username='admin', full_name='Admin', password='AdminPass123!'))"

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v
```

**Acceder a servicios:**
- API: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050`

---

## 📦 Dependencias del Proyecto

### Dependencias de Producción
- `fastapi[all]` - Framework web moderno y rápido
- `uvicorn[standard]` - Servidor ASGI de alto rendimiento
- `sqlalchemy` - ORM para base de datos
- `pydantic` - Validación de datos y serialización
- `pydantic-settings` - Gestión de configuraciones desde variables de entorno
- `python-dotenv` - Carga de variables de entorno desde archivos .env
- `passlib[bcrypt]` - Hashing seguro de contraseñas con bcrypt
- `python-jose[cryptography]` - Creación y validación de tokens JWT
- `python-multipart` - Soporte para form-data (requerido para login)
- `psycopg2-binary` - Driver PostgreSQL (opcional, para producción)

### Dependencias de Desarrollo
- `pytest` - Framework de testing
- `httpx` - Cliente HTTP para tests
- `pytest-cov` - Cobertura de tests
- `pytest-asyncio` - Soporte para tests asíncronos

### Dependencias Opcionales (Mejoras Futuras)
- `alembic` - Migraciones de base de datos
- `slowapi` - Rate limiting
- `redis` - Cache y sesiones
- `celery` - Tareas asíncronas
- `sentry-sdk` - Monitoreo de errores

---

## 🔧 Comandos Útiles

### Gestión del Entorno Virtual
```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Desactivar entorno virtual
deactivate

# Listar paquetes instalados
uv pip list

# Actualizar pip
uv pip install --upgrade pip
```

### Desarrollo
```powershell
# Ejecutar aplicación en modo desarrollo (auto-reload)
uvicorn app.main:app --reload

# Ejecutar en puerto específico
uvicorn app.main:app --reload --port 8001

# Ejecutar tests
pytest tests/ -v

# Ejecutar tests con cobertura
pytest tests/ --cov=app --cov-report=term-missing
```

### Base de Datos
```powershell
# Crear migraciones (si se usa Alembic)
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head

# Revertir migraciones
alembic downgrade -1
```

---

## 📊 Criterios de Éxito

### Infraestructura
- [ ] Entorno virtual configurado y funcionando
- [ ] Dependencias instaladas con UV
- [ ] Estructura de proyecto organizada
- [ ] Base de datos configurada y conectada

### Seguridad y Autenticación
- [ ] Funciones de hashing de contraseñas implementadas (bcrypt)
- [ ] Generación y validación de tokens JWT funcionando
- [ ] Dependencias de autenticación (get_current_user) implementadas
- [ ] SECRET_KEY segura generada y configurada
- [ ] Contraseñas nunca expuestas en responses

### Modelos y Schemas
- [ ] Modelo User con todos los campos implementado
- [ ] Schemas de Usuario (Create, Update, Response) implementados
- [ ] Schemas de Autenticación (Login, Token) implementados
- [ ] Validaciones de Pydantic funcionando correctamente

### Servicios de Negocio
- [ ] Servicio de autenticación completo (login, register, refresh)
- [ ] Servicio CRUD de usuarios completo
- [ ] Logging exhaustivo en todos los servicios
- [ ] Manejo de errores apropiado

### Endpoints
- [ ] Endpoints de autenticación funcionando (register, login, refresh, me)
- [ ] Endpoints CRUD de usuarios funcionando
- [ ] Autorización basada en roles implementada
- [ ] Usuarios pueden gestionar su propio perfil
- [ ] Admins pueden gestionar todos los usuarios
- [ ] Documentación OpenAPI completa y accesible

### Testing
- [ ] Tests de autenticación implementados
- [ ] Tests CRUD de usuarios implementados
- [ ] Tests de autorización por roles
- [ ] Cobertura de tests > 80%

### Ejecución
- [ ] Aplicación ejecutándose correctamente
- [ ] Login y registro funcionando en Swagger UI
- [ ] Endpoints protegidos requiriendo JWT
- [ ] Logging visible en consola
- [ ] Manejo de errores robusto
- [ ] Usuario superadmin creado automáticamente

### Docker (Fase Final)
- [ ] Dockerfile creado y optimizado
- [ ] docker-compose.yml con API + PostgreSQL + pgAdmin
- [ ] Aplicación ejecutándose en contenedores
- [ ] Variables de entorno configuradas para Docker

---

## 🚀 Próximos Pasos Después de Completar el Plan

1. **Migraciones de Base de Datos:** Implementar Alembic para gestionar cambios en esquema de forma versionada
2. **Email Verification:** Sistema de verificación de email con tokens de activación
3. **Password Recovery:** Recuperación de contraseña mediante email
4. **Two-Factor Authentication (2FA):** Autenticación de dos factores con TOTP
5. **Rate Limiting:** Protección contra ataques de fuerza bruta y abuso
6. **Caching con Redis:** Mejorar rendimiento con cache de sesiones y datos frecuentes
7. **Monitoreo:** Implementar Prometheus, Grafana o Sentry para monitoreo en producción
8. **CI/CD:** Configurar pipeline con GitHub Actions o GitLab CI
9. **Deploy a Producción:** Desplegar en AWS, Google Cloud, Azure, o plataformas como Railway/Render
10. **WebSockets:** Notificaciones en tiempo real (opcional)

---

## 📚 Referencias y Documentación

### Frameworks y Librerías
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación oficial completa
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - Guía de seguridad y OAuth2
- [Pydantic Documentation](https://docs.pydantic.dev/) - Validación de datos
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) - ORM

### Seguridad
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Principales riesgos de seguridad
- [JWT.io](https://jwt.io/) - Información sobre JSON Web Tokens
- [Passlib Documentation](https://passlib.readthedocs.io/) - Hashing de contraseñas

### Herramientas
- [UV Documentation](https://github.com/astral-sh/uv) - Gestor de paquetes rápido
- [Docker Documentation](https://docs.docker.com/) - Contenerización
- [Pytest Documentation](https://docs.pytest.org/) - Testing

### Tutoriales y Guías
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - Mejores prácticas
- [Real Python FastAPI](https://realpython.com/fastapi-python-web-apis/) - Tutorial completo

---

## 🐛 Troubleshooting

### Error: "uv no se reconoce como comando"
**Solución:** Reiniciar PowerShell o agregar UV al PATH manualmente
```powershell
# Verificar instalación
where.exe uv
```

### Error: "No se puede ejecutar scripts en este sistema"
**Solución:** Configurar política de ejecución de PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "Puerto 8000 ya está en uso"
**Solución:** Cambiar puerto o detener proceso que lo usa:
```powershell
# Ver proceso en puerto 8000
netstat -ano | findstr :8000

# Detener proceso (reemplazar PID)
taskkill /PID <PID> /F
```

### Error: "401 Unauthorized" al acceder a endpoints protegidos
**Causas posibles:**
1. Token JWT no enviado o mal formateado
2. Token expirado
3. SECRET_KEY incorrecta o cambiada

**Solución:**
```powershell
# Verificar que el header Authorization esté correcto
# Formato: "Bearer <token>"

# Generar nuevo token haciendo login
$loginBody = @{
    email = "usuario@ejemplo.com"
    password = "Password123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/auth/login" -ContentType "application/json" -Body $loginBody
$token = $response.access_token
```

### Error: "422 Unprocessable Entity" en registro
**Causa:** Contraseña no cumple requisitos de seguridad

**Solución:** Asegurar que la contraseña tenga:
- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 número
- (Opcional) Al menos 1 carácter especial

### Error: "409 Conflict" - Email o username ya existe
**Solución:** Usar un email/username diferente o eliminar el usuario existente desde admin

### Error: "Could not validate credentials"
**Causa:** Token JWT inválido o SECRET_KEY incorrecta

**Solución:**
1. Verificar que SECRET_KEY en .env sea la misma que se usó para generar el token
2. Generar nuevo token con login
3. Verificar que el token no esté cortado o modificado

### Error de dependencias con bcrypt en Windows
**Solución:** Instalar Visual C++ Build Tools:
```powershell
# Alternativamente, usar wheels pre-compilados
uv pip install --only-binary :all: passlib[bcrypt]
```

### Error: Base de datos locked (SQLite)
**Causa:** Múltiples procesos intentando acceder a SQLite simultáneamente

**Solución:**
1. Usar PostgreSQL para desarrollo con múltiples workers
2. O ejecutar con un solo worker:
```powershell
uvicorn app.main:app --reload --workers 1
```

---

## 📝 Notas Importantes

### Seguridad
- **SECRET_KEY:** NUNCA usar la clave por defecto en producción. Generar con `secrets.token_urlsafe(32)`
- **Contraseñas:** NUNCA almacenar contraseñas en texto plano. Siempre usar bcrypt
- **Tokens JWT:** Configurar tiempo de expiración apropiado (30 min access, 7 días refresh)
- **Variables de entorno:** NUNCA commitear el archivo `.env` con claves reales
- **HTTPS:** En producción, SIEMPRE usar HTTPS (certificados SSL/TLS)
- **Validación:** Validar y sanitizar TODOS los inputs del usuario
- **Logs:** NO logear información sensible (passwords, tokens completos)

### Desarrollo
- **Logging exhaustivo:** Implementar logs en cada capa para facilitar debugging
- **Sin scripts:** Todos los comandos se ejecutan directamente en PowerShell
- **Formato de código:** Seguir convenciones de estilo consistentes (evitar saltos de línea excesivos en anotaciones)
- **Tests primero:** Escribir tests antes de implementar funcionalidades complejas
- **Documentación OpenAPI:** Mantener actualizada con cada cambio en endpoints
- **Git:** NO commitear archivos `.env`, `__pycache__/`, `.venv/`, `*.pyc`

### Base de Datos
- **SQLite:** Solo para desarrollo y testing
- **PostgreSQL:** Recomendado para producción
- **Migraciones:** Usar Alembic para cambios en esquema en producción
- **Backups:** Implementar estrategia de respaldo en producción

### Autenticación
- **Roles:** Implementar control de acceso basado en roles (RBAC)
- **Permisos:** Usuario solo puede editar su propio perfil, admin puede gestionar todos
- **Token Refresh:** Implementar mecanismo de refresh token para mejor UX
- **Logout:** Considerar implementar blacklist de tokens para logout real

### Buenas Prácticas
- **Principio de mínimo privilegio:** Usuario normal no debe tener permisos de admin
- **Fail securely:** En caso de error, fallar de forma segura (denegar acceso)
- **Auditoría:** Registrar operaciones sensibles (cambios de contraseña, creación/eliminación de usuarios)
- **Rate Limiting:** Implementar límites de requests para prevenir abuso
- **CORS:** Configurar CORS solo para orígenes confiables

---

## 🔐 Checklist de Seguridad Pre-Producción

Antes de desplegar a producción, verificar:

- [ ] SECRET_KEY generada con método criptográficamente seguro
- [ ] DEBUG = False en producción
- [ ] HTTPS configurado (certificado SSL válido)
- [ ] CORS configurado con orígenes específicos (no usar "*")
- [ ] Rate limiting implementado
- [ ] Logs configurados sin exponer información sensible
- [ ] Validaciones de entrada en todos los endpoints
- [ ] Tests de seguridad ejecutados (OWASP Top 10)
- [ ] Base de datos con credenciales seguras
- [ ] Backups automáticos configurados
- [ ] Monitoreo y alertas configurados
- [ ] Documentación de API actualizada
- [ ] Plan de recuperación ante desastres documentado

---

**Fecha de creación:** 2025-11-10  
**Versión:** 2.0  
**Estado:** Plan completo - Sistema de gestión de usuarios con autenticación segura  
**Última actualización:** 2025-11-10

