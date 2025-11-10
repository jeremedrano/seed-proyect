"""
Caso de uso: Crear Usuario.

Contiene la lógica de negocio para crear un nuevo usuario.
Valida los datos y coordina con el repositorio.
"""
import logging
import re
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

LOG = logging.getLogger(__name__)


class CreateUserUseCase:
    """
    Caso de uso para crear un nuevo usuario en el sistema.
    
    Responsabilidades:
    - Validar datos de entrada
    - Verificar que el email no exista
    - Crear entidad User
    - Guardar en repositorio
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            user_repository: Repositorio de usuarios (puerto/interfaz)
        """
        self.user_repository = user_repository
    
    def execute(self, email: str, name: str, age: int) -> User:
        """
        Ejecuta el caso de uso de crear usuario.
        
        Args:
            email: Email del usuario
            name: Nombre del usuario
            age: Edad del usuario
            
        Returns:
            User: Usuario creado con ID asignado
            
        Raises:
            ValueError: Si los datos son inválidos o el email ya existe
        """
        LOG.info("Use case: CreateUser - Starting for email=%s", email)
        
        # Validación: nombre no vacío
        if not name or name.strip() == "":
            LOG.warning("Use case: CreateUser - Name is empty")
            raise ValueError("Name cannot be empty")
        
        # Validación: formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            LOG.warning("Use case: CreateUser - Invalid email format: %s", email)
            raise ValueError("Invalid email format")
        
        # Validación: edad positiva
        if age <= 0:
            LOG.warning("Use case: CreateUser - Age must be positive: %d", age)
            raise ValueError("Age must be positive")
        
        # Verificar que el email no exista
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            LOG.warning("Use case: CreateUser - Email already exists: %s", email)
            raise ValueError("Email already exists")
        
        # Crear entidad User (sin ID)
        user = User(id=None, email=email, name=name, age=age)
        LOG.debug("Use case: CreateUser - User entity created: %s", user)
        
        # Guardar en repositorio
        saved_user = self.user_repository.save(user)
        LOG.info("Use case: CreateUser - User saved with id=%s", saved_user.id)
        
        return saved_user

