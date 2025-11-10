"""
Configuración de fixtures de pytest para todos los tests.

Fixtures compartidos entre tests unitarios, de integración y e2e.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.infrastructure.database.models.base import Base


@pytest.fixture(scope="function")
def db_engine():
    """
    Crea un engine de SQLAlchemy con SQLite en memoria.
    
    Scope: function - Se crea una DB nueva para cada test (aislamiento).
    """
    # SQLite en memoria - no requiere instalación
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,  # True para debug SQL
        connect_args={"check_same_thread": False}
    )
    
    # Crear todas las tablas
    Base.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup - drop todas las tablas
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Session:
    """
    Crea una sesión de SQLAlchemy para tests.
    
    Scope: function - Sesión nueva para cada test.
    Hace rollback automático al finalizar el test.
    """
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    
    yield session
    
    # Cleanup - rollback y close
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def sample_user_data():
    """
    Datos de ejemplo para crear usuarios en tests.
    
    Returns:
        dict: Datos de un usuario de ejemplo
    """
    return {
        "email": "test@example.com",
        "name": "Test User",
        "age": 25
    }


@pytest.fixture(scope="function")
def sample_users_data():
    """
    Múltiples usuarios de ejemplo para tests.
    
    Returns:
        list[dict]: Lista de datos de usuarios
    """
    return [
        {"email": "user1@example.com", "name": "User One", "age": 20},
        {"email": "user2@example.com", "name": "User Two", "age": 30},
        {"email": "user3@example.com", "name": "User Three", "age": 40},
    ]

