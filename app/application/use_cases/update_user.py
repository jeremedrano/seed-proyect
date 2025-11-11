"""
Caso de uso: Actualizar Usuario.

Contiene la lógica de negocio para actualizar un usuario existente.
"""
import logging
import re
from typing import Optional
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

LOG = logging.getLogger(__name__)


class UpdateUserUseCase:
    """
    Caso de uso para actualizar un usuario existente.
    
    Responsabilidades:
    - Validar que el usuario exista
    - Validar datos de entrada (solo los proporcionados)
    - Verificar que el email no esté en uso por otro usuario
    - Actualizar el usuario en el repositorio
    """
    
    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            user_repository: Repositorio de usuarios (puerto/interfaz)
        """
        self.user_repository = user_repository
    
    def execute(
        self,
        user_id: int,
        email: Optional[str] = None,
        name: Optional[str] = None,
        age: Optional[int] = None
    ) -> User:
        """
        Ejecuta el caso de uso de actualizar un usuario.
        
        Args:
            user_id: ID del usuario a actualizar
            email: Nuevo email (opcional)
            name: Nuevo nombre (opcional)
            age: Nueva edad (opcional)
            
        Returns:
            User: Usuario actualizado
            
        Raises:
            ValueError: Si el ID es inválido, el usuario no existe, o los datos son inválidos
        """
        LOG.info("-" * 60)
        LOG.info("Use case: UpdateUser - STARTING")
        LOG.info("-" * 60)
        LOG.info("Input parameters:")
        LOG.info("  - user_id: %s", user_id)
        LOG.info("  - email: %s", email if email else "(not provided)")
        LOG.info("  - name: %s", name if name else "(not provided)")
        LOG.info("  - age: %s", age if age is not None else "(not provided)")
        
        # Validación: ID positivo
        LOG.debug("Use case: Validating user_id...")
        if user_id <= 0:
            LOG.warning("Use case: UpdateUser - VALIDATION FAILED: User ID must be positive: %d", user_id)
            raise ValueError("User ID must be positive")
        LOG.debug("Use case: User ID validation passed")
        
        # Validación: Al menos un campo debe ser proporcionado
        if email is None and name is None and age is None:
            LOG.warning("Use case: UpdateUser - VALIDATION FAILED: No fields provided for update")
            raise ValueError("At least one field must be provided for update")
        
        # Buscar usuario existente
        LOG.info("Use case: Fetching existing user with ID: %d", user_id)
        existing_user = self.user_repository.get_by_id(user_id)
        
        if existing_user is None:
            LOG.warning("Use case: UpdateUser - NOT FOUND: User with ID %d not found", user_id)
            raise ValueError(f"User with ID {user_id} not found")
        
        LOG.info("Use case: User found - Current data:")
        LOG.info("  - Email: %s", existing_user.email)
        LOG.info("  - Name: %s", existing_user.name)
        LOG.info("  - Age: %s", existing_user.age)
        
        # Preparar datos actualizados (mantener los existentes si no se proporcionan nuevos)
        updated_email = email if email is not None else existing_user.email
        updated_name = name if name is not None else existing_user.name
        updated_age = age if age is not None else existing_user.age
        
        # Validaciones de los nuevos datos (solo si se proporcionaron)
        if email is not None:
            LOG.debug("Use case: Validating new email format...")
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                LOG.warning("Use case: UpdateUser - VALIDATION FAILED: Invalid email format: %s", email)
                raise ValueError("Invalid email format")
            LOG.debug("Use case: Email format validation passed")
            
            # Verificar que el email no esté en uso por otro usuario
            LOG.info("Use case: Checking if new email is available...")
            user_with_email = self.user_repository.get_by_email(email)
            if user_with_email and user_with_email.id != user_id:
                LOG.warning("Use case: UpdateUser - VALIDATION FAILED: Email already exists for another user")
                LOG.warning("  - Email: %s", email)
                LOG.warning("  - Existing user ID: %s", user_with_email.id)
                raise ValueError("Email already exists")
            LOG.info("Use case: Email is available or same as current")
        
        if name is not None:
            LOG.debug("Use case: Validating new name...")
            if not name or name.strip() == "":
                LOG.warning("Use case: UpdateUser - VALIDATION FAILED: Name cannot be empty")
                raise ValueError("Name cannot be empty")
            LOG.debug("Use case: Name validation passed")
        
        if age is not None:
            LOG.debug("Use case: Validating new age...")
            if age <= 0:
                LOG.warning("Use case: UpdateUser - VALIDATION FAILED: Age must be positive: %d", age)
                raise ValueError("Age must be positive")
            LOG.debug("Use case: Age validation passed")
        
        # Crear entidad User actualizada
        LOG.info("Use case: Creating updated User entity...")
        updated_user = User(
            id=user_id,
            email=updated_email,
            name=updated_name,
            age=updated_age
        )
        LOG.info("Use case: Updated User entity created")
        LOG.info("  - New email: %s", updated_user.email)
        LOG.info("  - New name: %s", updated_user.name)
        LOG.info("  - New age: %s", updated_user.age)
        
        # Actualizar en repositorio
        LOG.info("Use case: Calling repository.update()...")
        result = self.user_repository.update(updated_user)
        LOG.info("Use case: User updated successfully in repository")
        LOG.info("  - ID: %s", result.id)
        LOG.info("  - Email: %s", result.email)
        LOG.info("  - Name: %s", result.name)
        LOG.info("  - Age: %s", result.age)
        
        LOG.info("-" * 60)
        LOG.info("Use case: UpdateUser - COMPLETED SUCCESSFULLY")
        LOG.info("-" * 60)
        
        return result

