"""
Dependencias de FastAPI para inyección de dependencias.

Estas funciones se usan con Depends() en los endpoints.
"""
import logging
from typing import Generator
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.application.use_cases.get_all_users import GetAllUsersUseCase

LOG = logging.getLogger(__name__)

# TODO: Mover esto a config
DATABASE_URL = "sqlite:///./users.db"

LOG.info("Initializing database configuration...")
LOG.info("  - Database URL: %s", DATABASE_URL)

# Engine de SQLAlchemy (singleton)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo para SQLite
)

LOG.info("✅ SQLAlchemy engine created successfully")
LOG.info("  - Engine: %s", str(engine.url))
LOG.info("  - Dialect: %s", engine.dialect.name)

# SessionLocal factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

LOG.info("✅ SessionLocal factory configured")
LOG.info("  - Autocommit: False")
LOG.info("  - Autoflush: False")


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
    LOG.debug("Dependencies: Creating new database session")
    db = SessionLocal()
    LOG.debug("Dependencies: Database session created (id: %s)", id(db))
    try:
        yield db
    finally:
        LOG.debug("Dependencies: Closing database session (id: %s)", id(db))
        db.close()
        LOG.debug("Dependencies: Database session closed")


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
    LOG.debug("Dependencies: Creating UserRepositoryImpl instance")
    repository = UserRepositoryImpl(db)
    LOG.debug("Dependencies: UserRepositoryImpl created (id: %s)", id(repository))
    return repository


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
    LOG.debug("Dependencies: Creating CreateUserUseCase instance")
    use_case = CreateUserUseCase(repository)
    LOG.debug("Dependencies: CreateUserUseCase created (id: %s)", id(use_case))
    return use_case


def get_get_user_use_case(
    repository: UserRepositoryImpl = Depends(get_user_repository)
) -> GetUserUseCase:
    """
    Dependencia que provee el caso de uso GetUser.
    
    Args:
        repository: Repositorio de usuarios (inyectado automáticamente)
        
    Returns:
        GetUserUseCase: Instancia del caso de uso
        
    Usage:
        @app.get("/users/{user_id}")
        def get_user(use_case: GetUserUseCase = Depends(get_get_user_use_case)):
            ...
    """
    LOG.debug("Dependencies: Creating GetUserUseCase instance")
    use_case = GetUserUseCase(repository)
    LOG.debug("Dependencies: GetUserUseCase created (id: %s)", id(use_case))
    return use_case


def get_get_all_users_use_case(
    repository: UserRepositoryImpl = Depends(get_user_repository)
) -> GetAllUsersUseCase:
    """
    Dependencia que provee el caso de uso GetAllUsers.
    
    Args:
        repository: Repositorio de usuarios (inyectado automáticamente)
        
    Returns:
        GetAllUsersUseCase: Instancia del caso de uso
        
    Usage:
        @app.get("/users/")
        def get_all_users(use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case)):
            ...
    """
    LOG.debug("Dependencies: Creating GetAllUsersUseCase instance")
    use_case = GetAllUsersUseCase(repository)
    LOG.debug("Dependencies: GetAllUsersUseCase created (id: %s)", id(use_case))
    return use_case

