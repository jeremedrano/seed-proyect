"""
Dependencias de FastAPI para inyección de dependencias.

Estas funciones se usan con Depends() en los endpoints.
"""
from typing import Generator
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.create_user import CreateUserUseCase

# TODO: Mover esto a config
DATABASE_URL = "sqlite:///./users.db"

# Engine de SQLAlchemy (singleton)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia que provee una sesión de DB.
    
    Yields:
        Session: Sesión de SQLAlchemy
        
    Usage:
        @app.get("/users/")
        def get_users(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepositoryImpl:
    """
    Dependencia que provee el repositorio de usuarios.
    
    Args:
        db: Sesión de DB (inyectada automáticamente)
        
    Returns:
        UserRepositoryImpl: Instancia del repositorio
        
    Usage:
        @app.get("/users/")
        def get_users(repo: UserRepositoryImpl = Depends(get_user_repository)):
            ...
    """
    return UserRepositoryImpl(db)


def get_create_user_use_case(
    repository: UserRepositoryImpl = Depends(get_user_repository)
) -> CreateUserUseCase:
    """
    Dependencia que provee el caso de uso CreateUser.
    
    Args:
        repository: Repositorio de usuarios (inyectado automáticamente)
        
    Returns:
        CreateUserUseCase: Instancia del caso de uso
        
    Usage:
        @app.post("/users/")
        def create_user(use_case: CreateUserUseCase = Depends(get_create_user_use_case)):
            ...
    """
    return CreateUserUseCase(repository)

