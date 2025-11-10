# Plan de Trabajo: CRUD de Usuarios con FastAPI y UV (PoC)

## 📋 Descripción del Proyecto
Desarrollo de una **Prueba de Concepto (PoC)** de API REST con operaciones **CRUD de usuarios**, utilizando FastAPI con **Clean Architecture**, gestión de dependencias con UV, ejecución en entorno virtual (VENV). 

**Versión simplificada:** Sin autenticación en fase inicial, enfocado en implementar rápidamente el CRUD básico con arquitectura extensible.

**Filosofía de Desarrollo:** **TDD (Test-Driven Development)** - Escribir tests antes del código de implementación.

---

## 🎯 Objetivos del Proyecto (PoC)

1. ✅ Implementar CRUD completo de usuarios (Create, Read, Update, Delete)
2. ✅ Usar Clean Architecture para extensibilidad futura
3. ✅ Usar UV para gestión rápida de paquetes y entorno virtual
4. ✅ Documentación automática con OpenAPI/Swagger
5. ✅ Tests básicos (unit y e2e)
6. 🔜 (Futuro) Agregar autenticación JWT cuando sea necesario
7. 🔜 (Futuro) Contenerización con Docker

**Nota:** UV es una herramienta que reemplaza a `pip` y gestiona entornos virtuales de forma más rápida.

---

## 📐 Arquitectura Propuesta: Clean Architecture Simplificada

Clean Architecture **simplificada para PoC**, manteniendo extensibilidad para el futuro.

### **Principios de la Arquitectura:**
1. **Separación de capas:** Domain, Application, Infrastructure, Presentation
2. **Testabilidad:** Cada capa se puede testear independientemente
3. **Extensible:** Fácil agregar autenticación/compliance después
4. **Simple para empezar:** Solo lo necesario para CRUD de usuarios

### **Estructura Simplificada (PoC):**

```
seed-proyect/
├── app/
│   ├── __init__.py
│   ├── main.py                          # Punto de entrada FastAPI
│   │
│   ├── domain/                          # CAPA DE DOMINIO (lógica de negocio)
│   │   ├── __init__.py
│   │   ├── entities/
│   │   │   ├── __init__.py
│   │   │   └── user.py                  # Entidad User (modelo de dominio)
│   │   ├── repositories/                # Interfaces (Puertos)
│   │   │   ├── __init__.py
│   │   │   └── user_repository.py       # Interface UserRepository
│   │   └── exceptions/
│   │       ├── __init__.py
│   │       └── user_exceptions.py       # Excepciones personalizadas
│   │
│   ├── application/                     # CAPA DE APLICACIÓN (casos de uso)
│   │   ├── __init__.py
│   │   ├── use_cases/
│   │   │   ├── __init__.py
│   │   │   ├── create_user.py          # Caso de uso: Crear usuario
│   │   │   ├── get_user.py             # Caso de uso: Obtener usuario
│   │   │   ├── update_user.py          # Caso de uso: Actualizar usuario
│   │   │   ├── delete_user.py          # Caso de uso: Eliminar usuario
│   │   │   └── list_users.py           # Caso de uso: Listar usuarios
│   │   └── dto/
│   │       ├── __init__.py
│   │       └── user_dto.py             # DTOs para transferencia de datos
│   │
│   ├── infrastructure/                  # CAPA DE INFRAESTRUCTURA (adaptadores)
│   │   ├── __init__.py
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── config.py               # Configuración SQLAlchemy
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   └── user_model.py       # Modelo ORM SQLAlchemy
│   │   │   └── repositories/
│   │   │       ├── __init__.py
│   │   │       └── user_repository_impl.py  # Implementación del repositorio
│   │   └── logging/
│   │       ├── __init__.py
│   │       └── logger_config.py
│   │
│   ├── presentation/                    # CAPA DE PRESENTACIÓN (API)
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── endpoints/
│   │   │       │   ├── __init__.py
│   │   │       │   └── users.py        # Endpoints CRUD de usuarios
│   │   │       ├── dependencies.py     # Dependencies de FastAPI
│   │   │       └── router.py           # Router principal v1
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── user_schema.py          # Schemas Pydantic para validación
│   │   └── middleware/
│   │       ├── __init__.py
│   │       └── error_handler.py
│   │
│   └── config/
│       ├── __init__.py
│       └── settings.py                  # Configuraciones con Pydantic
│
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_user_use_cases.py
│   └── e2e/
│       ├── __init__.py
│       └── test_user_endpoints.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

### **Flujo de Dependencias:**
```
Presentation → Application → Domain ← Infrastructure
   (API)       (Use Cases)   (Entities)  (Database)
```

**Nota:** Arquitectura lista para extender con autenticación, compliance, etc. cuando sea necesario.

---

## 🧩 Ventajas de Clean Architecture (Incluso para PoC)

### ✅ **Extensibilidad:**
- **Agregar autenticación después:** Sin tocar código existente
- **Agregar nuevos módulos** (compliance, productos, etc.) es simple
- **Versionar API:** Fácil crear `api/v2/` cuando sea necesario

### ✅ **Mantenibilidad:**
- **Separación clara:** Cada capa tiene un propósito específico
- **Cambios localizados:** Cambiar DB no afecta lógica de negocio
- **Código limpio:** Fácil de entender y modificar

### ✅ **Testabilidad:**
- **Tests unitarios rápidos:** Use cases sin depender de DB
- **Mocks fáciles:** Interfaces permiten sustituir implementaciones
- **Tests aislados:** Cada capa se prueba independientemente

---

## 🔌 Ejemplo Rápido: Flujo de Crear Usuario

### **1. Domain (Entidad)**
```python
# app/domain/entities/user.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Entidad de dominio"""
    id: Optional[int]
    email: str
    name: str
    age: int
    
    def is_adult(self) -> bool:
        """Lógica de negocio"""
        return self.age >= 18
```

### **2. Application (Caso de Uso)**
```python
# app/application/use_cases/create_user.py
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, email: str, name: str, age: int) -> User:
        # Validaciones
        if age < 0:
            raise ValueError("Age must be positive")
        
        # Crear entidad
        user = User(id=None, email=email, name=name, age=age)
        
        # Guardar
        return self.repository.save(user)
```

### **3. Infrastructure (Repositorio)**
```python
# app/infrastructure/database/repositories/user_repository_impl.py
from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User
from app.infrastructure.database.models.user_model import UserModel

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, user: User) -> User:
        db_user = UserModel(email=user.email, name=user.name, age=user.age)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User(id=db_user.id, email=db_user.email, name=db_user.name, age=db_user.age)
```

### **4. Presentation (API)**
```python
# app/presentation/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends
from app.application.use_cases.create_user import CreateUserUseCase
from app.presentation.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    data: UserCreate,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    user = use_case.execute(data.email, data.name, data.age)
    return UserResponse.from_entity(user)
```

### **Flujo Completo:**
```
1. HTTP POST /api/v1/users
   ↓
2. Endpoint llama al Use Case
   ↓
3. Use Case crea la entidad User
   ↓
4. Use Case llama al Repository
   ↓
5. Repository guarda en DB (SQLAlchemy)
   ↓
6. Respuesta JSON al cliente
```

**Ventaja:** Puedes agregar autenticación después sin tocar esta lógica. ✅

---

## 🧪 Filosofía TDD (Test-Driven Development)

Este proyecto sigue la metodología **TDD**: escribir tests **ANTES** de implementar el código.

### **Ciclo TDD (Red-Green-Refactor):**

```
1. 🔴 RED: Escribir test que falla
   ↓
2. 🟢 GREEN: Escribir código mínimo para pasar el test
   ↓
3. 🔵 REFACTOR: Mejorar el código manteniendo tests verdes
   ↓
   Repetir...
```

### **Aplicando TDD por Capas:**

#### **1. Domain Layer (Tests Unitarios Puros)**
```python
# tests/unit/test_user_entity.py
def test_user_is_adult():
    # 🔴 RED: Test primero
    user = User(id=1, email="test@test.com", name="Test", age=20)
    assert user.is_adult() == True

# Luego implementar User.is_adult() en domain/entities/user.py
```

#### **2. Application Layer (Tests de Use Cases)**
```python
# tests/unit/test_create_user_use_case.py
def test_create_user_saves_to_repository():
    # 🔴 RED: Test con mock
    mock_repo = Mock(spec=UserRepository)
    use_case = CreateUserUseCase(mock_repo)
    
    user = use_case.execute("test@test.com", "Test", 25)
    
    mock_repo.save.assert_called_once()

# Luego implementar CreateUserUseCase.execute()
```

#### **3. Infrastructure Layer (Tests de Integración)**
```python
# tests/integration/test_user_repository.py
def test_user_repository_saves_and_retrieves(db_session):
    # 🔴 RED: Test con DB real (en memoria)
    repo = UserRepositoryImpl(db_session)
    user = User(id=None, email="test@test.com", name="Test", age=25)
    
    saved_user = repo.save(user)
    
    assert saved_user.id is not None
    assert saved_user.email == "test@test.com"

# Luego implementar UserRepositoryImpl
```

#### **4. Presentation Layer (Tests E2E)**
```python
# tests/e2e/test_user_endpoints.py
def test_create_user_endpoint(client):
    # 🔴 RED: Test del endpoint
    response = client.post("/api/v1/users/", json={
        "email": "test@test.com",
        "name": "Test User",
        "age": 25
    })
    
    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"

# Luego implementar el endpoint en presentation/api/v1/endpoints/users.py
```

### **Orden de Implementación con TDD:**

Para cada funcionalidad (ej: CreateUser):

1. **Test Domain:** Entidad User
2. **Test Application:** CreateUserUseCase
3. **Test Infrastructure:** UserRepositoryImpl
4. **Test Presentation:** POST /users endpoint

**Resultado:** Cada capa tiene tests antes de implementarse. ✅

### **Comandos para Ejecutar Tests:**

```powershell
# Ejecutar todos los tests
pytest

# Ejecutar solo tests unitarios (rápidos) - por directorio
pytest tests/unit/ -v

# Ejecutar solo tests unitarios - por marker
pytest -m unit

# Ejecutar tests de integración
pytest -m integration

# Ejecutar tests e2e
pytest -m e2e

# Excluir tests lentos (desarrollo rápido)
pytest -m "not slow"

# Ejecutar con cobertura
pytest --cov=app --cov-report=html

# Modo watch (TDD) - re-ejecutar al guardar
ptw

# Watch solo tests unitarios
ptw -- -m unit

# Verificar cobertura mínima (80%)
pytest --cov=app --cov-fail-under=80
```

**Nota:** La configuración de pytest está en `pytest.ini` con opciones optimizadas para TDD.

### **Markers de Pytest (para organizar tests):**

Marca tus tests con decoradores para ejecutarlos selectivamente:

```python
import pytest

# Test unitario (rápido, sin DB)
@pytest.mark.unit
def test_user_entity():
    user = User(id=1, email="test@test.com", name="Test", age=25)
    assert user.is_adult() == True

# Test de integración (con DB)
@pytest.mark.integration
def test_user_repository(db_session):
    repo = UserRepositoryImpl(db_session)
    # ...

# Test e2e (API completa)
@pytest.mark.e2e
def test_create_user_endpoint(client):
    response = client.post("/api/v1/users/", json={...})
    # ...

# Test lento (puede omitirse en desarrollo)
@pytest.mark.slow
def test_heavy_operation():
    # Operación que tarda mucho...
    pass
```

### **Beneficios de TDD en Clean Architecture:**

✅ **Diseño emergente:** Los tests guían el diseño de interfaces  
✅ **Menos bugs:** Código cubierto desde el inicio  
✅ **Refactoring seguro:** Tests garantizan que no rompiste nada  
✅ **Documentación viva:** Los tests documentan cómo usar el código  
✅ **Desarrollo más rápido:** Detectas errores inmediatamente  

### **Estructura de Tests Esperada:**

```
tests/
├── conftest.py              # Fixtures compartidos (DB, cliente HTTP, mocks)
├── unit/                    # Tests rápidos sin dependencias
│   ├── domain/
│   │   └── test_user_entity.py
│   └── use_cases/
│       ├── test_create_user.py
│       ├── test_get_user.py
│       ├── test_update_user.py
│       ├── test_delete_user.py
│       └── test_list_users.py
├── integration/             # Tests con DB (SQLite en memoria)
│   └── test_user_repository.py
└── e2e/                     # Tests de API completa
    └── test_user_endpoints.py
```

**Fixtures importantes en `conftest.py`:**
- `db_session`: Sesión de base de datos (SQLite en memoria)
- `client`: Cliente HTTP de FastAPI para tests e2e
- `mock_user_repository`: Mock del repositorio para tests unitarios

---

## 🗓️ Plan de Trabajo Detallado

### **FASE 1: Configuración del Entorno de Desarrollo**

#### 1.1 Instalación de UV
**Objetivo:** Instalar UV (gestor de paquetes rápido que reemplaza pip)

**¿Qué es UV?**
- Herramienta escrita en Rust, mucho más rápida que pip
- Crea y gestiona entornos virtuales (venv)
- Instala paquetes Python
- Compatible con pip (usa `uv pip install` en vez de `pip install`)

**Comandos:**
```powershell
# Instalación de UV (Windows PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verificación:**
```powershell
uv --version
```

#### 1.2 Creación del Entorno Virtual con UV
**Objetivo:** Crear un entorno virtual aislado usando UV

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Crear entorno virtual (.venv) usando UV
uv venv

# Activar el entorno virtual
.\.venv\Scripts\Activate.ps1
```

**Resultado Esperado:**
- Directorio `.venv/` creado con Python aislado
- Prompt debe mostrar `(.venv)` al inicio
- UV puede instalar paquetes en este venv

#### 1.3 Instalación de Dependencias (Producción + TDD)
**Objetivo:** Instalar dependencias de producción y desarrollo para TDD

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Con entorno virtual activado

# Dependencias de producción
uv pip install fastapi
uv pip install uvicorn[standard]
uv pip install sqlalchemy
uv pip install python-dotenv
uv pip install pydantic
uv pip install pydantic-settings

# Dependencias de desarrollo (TDD)
uv pip install pytest
uv pip install httpx
uv pip install pytest-cov
uv pip install pytest-watch
uv pip install pytest-mock
```

**Justificación:**
- `fastapi`: Framework web
- `uvicorn[standard]`: Servidor ASGI
- `sqlalchemy`: ORM para base de datos
- `python-dotenv`: Variables de entorno
- `pydantic`: Validación de datos
- `pydantic-settings`: Configuración
- `pytest`: Framework de testing (TDD)
- `httpx`: Cliente HTTP para tests e2e
- `pytest-cov`: Cobertura de código
- `pytest-watch`: Auto-ejecutar tests al guardar (TDD workflow)
- `pytest-mock`: Mocking para tests unitarios

**Nota:** Con TDD, instalaremos las dependencias de testing desde el inicio.

#### 1.4 Generar archivo de dependencias
**Objetivo:** Documentar dependencias del proyecto

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
uv pip freeze > requirements.txt
```

---

### **FASE 2: Estructura Base del Proyecto (Simplificada)**

#### 2.1 Crear Estructura de Directorios
**Objetivo:** Crear estructura Clean Architecture simplificada para PoC

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Crear estructura simplificada
New-Item -ItemType Directory -Path `
    app, `
    app\domain, app\domain\entities, app\domain\repositories, app\domain\exceptions, `
    app\application, app\application\use_cases, app\application\dto, `
    app\infrastructure, app\infrastructure\database, app\infrastructure\database\models, app\infrastructure\database\repositories, app\infrastructure\logging, `
    app\presentation, app\presentation\api, app\presentation\api\v1, app\presentation\api\v1\endpoints, app\presentation\schemas, app\presentation\middleware, `
    app\config, `
    tests, tests\unit, tests\e2e `
    -Force
```

**Justificación Técnica:**
- **Domain:** Entidad User + Interface UserRepository
- **Application:** 5 Use Cases (create, get, update, delete, list)
- **Infrastructure:** Implementación del repositorio con SQLAlchemy
- **Presentation:** Endpoints REST para CRUD
- **Tests:** unit (sin DB) y e2e (con API)

#### 2.2 Crear Archivos __init__.py
**Objetivo:** Convertir directorios en paquetes Python

**Comandos desde:** `C:\workspace\seed-proyect`
```powershell
# Domain
New-Item -ItemType File -Path app\domain\__init__.py, app\domain\entities\__init__.py, app\domain\repositories\__init__.py, app\domain\exceptions\__init__.py

# Application
New-Item -ItemType File -Path app\application\__init__.py, app\application\use_cases\__init__.py, app\application\dto\__init__.py

# Infrastructure
New-Item -ItemType File -Path app\infrastructure\__init__.py, app\infrastructure\database\__init__.py, app\infrastructure\database\models\__init__.py, app\infrastructure\database\repositories\__init__.py, app\infrastructure\logging\__init__.py

# Presentation
New-Item -ItemType File -Path app\presentation\__init__.py, app\presentation\api\__init__.py, app\presentation\api\v1\__init__.py, app\presentation\api\v1\endpoints\__init__.py, app\presentation\schemas\__init__.py, app\presentation\middleware\__init__.py

# Config and tests
New-Item -ItemType File -Path app\config\__init__.py, app\__init__.py, tests\__init__.py, tests\unit\__init__.py, tests\e2e\__init__.py
```

**Resultado Esperado:**
- Estructura Clean Architecture lista para CRUD de usuarios
- Todos los directorios son paquetes Python válidos
- Simplificado pero extensible para el futuro

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
**Objetivo:** Centralizar variables de entorno (simplicado para PoC)

**Contenido de `.env`:**
```env
# Base de datos
DATABASE_URL=sqlite:///./app.db

# Configuración general
API_VERSION=v1
DEBUG=True
APP_NAME=Users CRUD API

# CORS (origenes permitidos)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

**Nota:** No incluimos variables de seguridad (JWT) en esta fase inicial del PoC.

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
uvicorn app.presentation.api.v1.main:app --reload --host 0.0.0.0 --port 8000
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
CMD ["uvicorn", "app.presentation.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]
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

## 📦 Dependencias del Proyecto (Simplificadas)

### Dependencias de Producción (PoC)
- `fastapi` - Framework web moderno y rápido
- `uvicorn[standard]` - Servidor ASGI de alto rendimiento
- `sqlalchemy` - ORM para base de datos
- `pydantic` - Validación de datos y serialización
- `pydantic-settings` - Gestión de configuraciones
- `python-dotenv` - Carga de variables de entorno

### Dependencias de Desarrollo (TDD)
- `pytest` - Framework de testing
- `httpx` - Cliente HTTP para tests
- `pytest-cov` - Cobertura de tests
- `pytest-watch` - Auto-ejecutar tests al guardar archivos (TDD)
- `pytest-mock` - Mocking para tests unitarios

### Para Agregar Después (Cuando sea necesario)
- `passlib[bcrypt]` - Hashing de contraseñas (cuando agregues autenticación)
- `python-jose[cryptography]` - Tokens JWT (cuando agregues autenticación)
- `python-multipart` - Soporte para form-data (cuando agregues autenticación)
- `alembic` - Migraciones de base de datos (para producción)
- `psycopg2-binary` - Driver PostgreSQL (para producción)

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
uvicorn app.presentation.api.v1.main:app --reload

# Ejecutar en puerto específico
uvicorn app.presentation.api.v1.main:app --reload --port 8001

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

## 📊 Criterios de Éxito (PoC Simplificado con TDD)

### Infraestructura
- [ ] Entorno virtual configurado y funcionando con UV
- [ ] Dependencias de producción instaladas (fastapi, uvicorn, sqlalchemy)
- [ ] Dependencias de testing instaladas (pytest, pytest-watch, pytest-mock)
- [ ] Estructura Clean Architecture creada
- [ ] Base de datos SQLite configurada
- [ ] Archivos `.cursorrules` y `pytest.ini` creados

### TDD Setup
- [ ] `pytest.ini` configurado con markers (unit, integration, e2e)
- [ ] `conftest.py` con fixtures básicos creado
- [ ] `pytest` se ejecuta sin errores (aunque no haya tests aún)
- [ ] `ptw` (pytest-watch) funciona en modo TDD

### Domain Layer
- [ ] Entidad User implementada (user.py)
- [ ] Interface UserRepository definida
- [ ] Excepciones personalizadas creadas

### Application Layer
- [ ] Use Case CreateUser implementado
- [ ] Use Case GetUser implementado
- [ ] Use Case UpdateUser implementado
- [ ] Use Case DeleteUser implementado
- [ ] Use Case ListUsers implementado

### Infrastructure Layer
- [ ] Modelo SQLAlchemy UserModel implementado
- [ ] UserRepositoryImpl implementado
- [ ] Configuración de base de datos (config.py)

### Presentation Layer
- [ ] Schemas Pydantic (UserCreate, UserUpdate, UserResponse)
- [ ] Endpoints CRUD implementados (POST, GET, PUT, DELETE)
- [ ] Router configurado y registrado
- [ ] Middleware de manejo de errores

### Ejecución
- [ ] Aplicación ejecutándose en http://localhost:8000
- [ ] Documentación Swagger accesible en /docs
- [ ] Crear usuario funciona correctamente
- [ ] Listar usuarios funciona correctamente
- [ ] Obtener usuario por ID funciona
- [ ] Actualizar usuario funciona
- [ ] Eliminar usuario funciona
- [ ] Logging visible en consola

### Testing (TDD - Tests escritos ANTES del código)
- [ ] Tests unitarios de entidad User (domain)
- [ ] Tests unitarios de Use Cases (application)
- [ ] Tests de integración de Repository (infrastructure)
- [ ] Tests e2e de endpoints (presentation)
- [ ] Todos los tests pasan (🟢 GREEN)
- [ ] Cobertura de código > 80%
- [ ] Cada funcionalidad implementada tiene test previo (TDD)

### Documentación
- [ ] README actualizado
- [ ] OpenAPI docs generados automáticamente
- [ ] Endpoints documentados con descripciones


---

## 🚀 Próximos Pasos Después de Completar el PoC

### **Fase 2 - Agregar Seguridad (Cuando sea necesario):**
1. **Autenticación JWT:** Login, tokens de acceso y refresh
2. **Hash de Contraseñas:** bcrypt/passlib para passwords
3. **Autorización por Roles:** user, admin, superadmin
4. **Proteger Endpoints:** Requerir autenticación en CRUD

### **Fase 3 - Preparar para Producción:**
5. **Migraciones con Alembic:** Control de versiones de DB
6. **PostgreSQL:** Cambiar de SQLite a PostgreSQL
7. **Docker:** Contenerización con docker-compose
8. **Tests Completos:** Aumentar cobertura > 80%

### **Fase 4 - Funcionalidades Avanzadas (Opcional):**
9. **Compliance/Auditoría:** Registros de operaciones
10. **Email Verification:** Validar emails con tokens
11. **Rate Limiting:** Protección contra abuso
12. **Monitoreo:** Sentry, Prometheus, Grafana
13. **CI/CD:** GitHub Actions para deployment automático

**Nota:** La arquitectura Clean está lista para soportar todas estas mejoras sin reescribir código existente. ✅

---

## 📚 Referencias y Documentación

### Frameworks y Librerías
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación oficial completa
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) - Guía de seguridad y OAuth2
- [Pydantic Documentation](https://docs.pydantic.dev/) - Validación de datos
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) - ORM

### Clean Architecture & Design Patterns
- [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Artículo original
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Ports & Adapters
- [Clean Architecture in Python](https://github.com/cosmic-python/book) - Libro gratuito
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/) - DI para Python
- [Martin Fowler - Application Architecture](https://martinfowler.com/architecture/) - Patterns

### Seguridad
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Principales riesgos de seguridad
- [JWT.io](https://jwt.io/) - Información sobre JSON Web Tokens
- [Passlib Documentation](https://passlib.readthedocs.io/) - Hashing de contraseñas
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/) - Estándares de autenticación


### Herramientas
- [UV Documentation](https://github.com/astral-sh/uv) - Gestor de paquetes rápido
- [Docker Documentation](https://docs.docker.com/) - Contenerización
- [Pytest Documentation](https://docs.pytest.org/) - Testing
- [Alembic](https://alembic.sqlalchemy.org/) - Migraciones de base de datos

### Tutoriales y Guías
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - Mejores prácticas
- [Real Python FastAPI](https://realpython.com/fastapi-python-web-apis/) - Tutorial completo
- [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-template) - Template oficial con buenas prácticas

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
uvicorn app.presentation.api.v1.main:app --reload --workers 1
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
**Versión:** 4.0 - PoC Simplificado  
**Arquitectura:** Clean Architecture (Simplificada)  
**Estado:** Prueba de Concepto - CRUD de usuarios sin autenticación  
**Última actualización:** 2025-11-10

---

## 📌 Resumen Ejecutivo

Este proyecto implementa una **Prueba de Concepto (PoC)** de CRUD de usuarios con:

✅ **CRUD completo** (Create, Read, Update, Delete, List)  
✅ **Clean Architecture** simplificada para extensibilidad  
✅ **Sin autenticación** en fase inicial (se puede agregar después)  
✅ **API RESTful** con FastAPI  
✅ **SQLite** para desarrollo rápido  
✅ **Documentación OpenAPI** automática  
✅ **Tests básicos** (unit y e2e)  

**Ideal para:** Prueba de concepto rápida con arquitectura extensible para agregar funcionalidades después.

**📋 Cursor Rules:** Este proyecto incluye un archivo `.cursorrules` con reglas de desarrollo TDD y Clean Architecture. Las reglas se aplican automáticamente en Cursor AI.

