"""
Aplicación principal de FastAPI.

Define la app de FastAPI y registra todos los routers.
"""
import logging
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.v1.endpoints import users
from app.infrastructure.database.models.base import Base
from app.presentation.api.v1.dependencies import engine

# Configurar logging exhaustivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)-35s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

LOG = logging.getLogger(__name__)

# Crear aplicación FastAPI
LOG.info("="*80)
LOG.info("Initializing FastAPI application...")
LOG.info("="*80)

app = FastAPI(
    title="User Management API",
    description="API REST para gestión de usuarios - PoC con Clean Architecture y TDD",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

LOG.info("FastAPI app created successfully")
LOG.info("  - Title: User Management API")
LOG.info("  - Version: 1.0.0")
LOG.info("  - Docs URL: /api/v1/docs")
LOG.info("  - ReDoc URL: /api/v1/redoc")

# Configurar CORS (para desarrollo)
LOG.info("Configuring CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restringir en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
LOG.info("CORS middleware configured (allow_origins=*)")

# Middleware para loggear todas las requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para loggear todas las requests HTTP."""
    LOG.info(f"Incoming request: {request.method} {request.url.path}")
    LOG.debug(f"  - Client: {request.client.host if request.client else 'unknown'}:{request.client.port if request.client else 'unknown'}")
    LOG.debug(f"  - Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    LOG.info(f"Response: {request.method} {request.url.path} -> Status: {response.status_code}")
    return response

# Registrar routers
LOG.info("Registering routers...")
app.include_router(
    users.router,
    prefix="/api/v1"
)
LOG.info("  - Users router registered at /api/v1")

# Eventos de aplicación
@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación."""
    LOG.info("="*80)
    LOG.info("APPLICATION STARTUP EVENT")
    LOG.info("="*80)
    LOG.info("Database engine: %s", str(engine.url))
    LOG.info("Creating database tables if they don't exist...")
    
    try:
        Base.metadata.create_all(bind=engine)
        LOG.info("✅ Database tables created/verified successfully")
    except Exception as e:
        LOG.error("❌ Error creating database tables: %s", str(e), exc_info=True)
        raise
    
    LOG.info("Application ready to accept connections")
    LOG.info("="*80)
    LOG.info("Available endpoints:")
    LOG.info("  - GET    /                    -> Root endpoint")
    LOG.info("  - GET    /health              -> Health check")
    LOG.info("  - GET    /api/v1/docs         -> Swagger UI")
    LOG.info("  - GET    /api/v1/redoc        -> ReDoc")
    LOG.info("  - POST   /api/v1/users/       -> Create user")
    LOG.info("  - GET    /api/v1/users/{id}   -> Get user by ID")
    LOG.info("  - GET    /api/v1/users/       -> Get all users (with pagination)")
    LOG.info("  - PUT    /api/v1/users/{id}   -> Update user")
    LOG.info("  - DELETE /api/v1/users/{id}   -> Delete user")
    LOG.info("="*80)

@app.on_event("shutdown")
async def shutdown_event():
    """Evento ejecutado al apagar la aplicación."""
    LOG.info("="*80)
    LOG.info("APPLICATION SHUTDOWN EVENT")
    LOG.info("="*80)
    LOG.info("Closing database connections...")
    engine.dispose()
    LOG.info("✅ Database connections closed")
    LOG.info("Application shutdown complete")
    LOG.info("="*80)

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status de la aplicación
    """
    LOG.debug("Health check requested")
    response = {"status": "healthy", "version": "1.0.0"}
    LOG.debug("Health check response: %s", response)
    return response


@app.get("/", tags=["root"])
def root():
    """
    Root endpoint.
    
    Returns:
        dict: Información básica de la API
    """
    LOG.debug("Root endpoint accessed")
    response = {
        "message": "User Management API",
        "version": "1.0.0",
        "docs": "/api/v1/docs"
    }
    LOG.debug("Root response: %s", response)
    return response


if __name__ == "__main__":
    import uvicorn
    LOG.info("Starting FastAPI application...")
    uvicorn.run(
        "app.presentation.api.v1.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

