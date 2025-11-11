"""
Caso de uso: Obtener Usuario por ID.

Contiene la lógica de negocio para obtener un usuario específico.
"""
import logging
from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

LOG = logging.getLogger(__name__)


class GetUserUseCase:
    """
    Caso de uso para obtener un usuario por su ID.
    
    Responsabilidades:
    - Validar que el ID sea válido
    - Buscar el usuario en el repositorio
    - Lanzar error si no existe
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            user_repository: Repositorio de usuarios (puerto/interfaz)
        """
        self.user_repository = user_repository
    
    def execute(self, user_id: int) -> User:
        """
        Ejecuta el caso de uso de obtener un usuario por ID.
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            User: Usuario encontrado
            
        Raises:
            ValueError: Si el ID es inválido o el usuario no existe
        """
        LOG.info("-" * 60)
        LOG.info("Use case: GetUser - STARTING")
        LOG.info("-" * 60)
        LOG.info("Input parameters:")
        LOG.info("  - user_id: %s", user_id)
        
        # Validación: ID positivo
        LOG.debug("Use case: Validating user_id...")
        if user_id <= 0:
            LOG.warning("Use case: GetUser - VALIDATION FAILED: User ID must be positive: %d", user_id)
            raise ValueError("User ID must be positive")
        LOG.debug("Use case: User ID validation passed")
        
        # Buscar usuario en repositorio
        LOG.info("Use case: Searching for user with ID: %d", user_id)
        user = self.user_repository.get_by_id(user_id)
        
        if user is None:
            LOG.warning("Use case: GetUser - NOT FOUND: User with ID %d not found", user_id)
            raise ValueError(f"User with ID {user_id} not found")
        
        LOG.info("Use case: User found successfully")
        LOG.info("  - ID: %s", user.id)
        LOG.info("  - Email: %s", user.email)
        LOG.info("  - Name: %s", user.name)
        LOG.info("  - Age: %s", user.age)
        
        LOG.info("-" * 60)
        LOG.info("Use case: GetUser - COMPLETED SUCCESSFULLY")
        LOG.info("-" * 60)
        
        return user

