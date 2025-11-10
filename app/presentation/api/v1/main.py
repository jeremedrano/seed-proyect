"""
Aplicación principal de FastAPI.

Define la app de FastAPI y registra todos los routers.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api.v1.endpoints import users
from app.infrastructure.database.models.base import Base
from app.presentation.api.v1.dependencies import engine

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOG = logging.getLogger(__name__)

# Crear aplicación FastAPI
app = FastAPI(
    title="User Management API",
    description="API REST para gestión de usuarios - PoC con Clean Architecture y TDD",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    openapi_url="/api/v1/openapi.json"
)

# Configurar CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restringir en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(
    users.router,
    prefix="/api/v1"
)

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status de la aplicación
    """
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/", tags=["root"])
def root():
    """
    Root endpoint.
    
    Returns:
        dict: Información básica de la API
    """
    return {
        "message": "User Management API",
        "version": "1.0.0",
        "docs": "/api/v1/docs"
    }


if __name__ == "__main__":
    import uvicorn
    LOG.info("Starting FastAPI application...")
    uvicorn.run(
        "app.presentation.api.v1.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

