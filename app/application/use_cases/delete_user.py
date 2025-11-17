"""
Caso de uso: Eliminar Usuario.

Contiene la lógica de negocio para eliminar un usuario existente.
"""

import logging

from app.domain.repositories.user_repository import UserRepository

LOG = logging.getLogger(__name__)


class DeleteUserUseCase:
    """
    Caso de uso para eliminar un usuario del sistema.

    Responsabilidades:
    - Validar que el ID sea válido
    - Verificar que el usuario exista
    - Eliminar el usuario del repositorio
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            user_repository: Repositorio de usuarios (puerto/interfaz)
        """
        self.user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        """
        Ejecuta el caso de uso de eliminar un usuario.

        Args:
            user_id: ID del usuario a eliminar

        Returns:
            bool: True si fue eliminado exitosamente

        Raises:
            ValueError: Si el ID es inválido o el usuario no existe
        """
        LOG.info("-" * 60)
        LOG.info("Use case: DeleteUser - STARTING")
        LOG.info("-" * 60)
        LOG.info("Input parameters:")
        LOG.info("  - user_id: %s", user_id)

        # Validación: ID positivo
        LOG.debug("Use case: Validating user_id...")
        if user_id <= 0:
            LOG.warning(
                "Use case: DeleteUser - VALIDATION FAILED: User ID must be positive: %d", user_id
            )
            raise ValueError("User ID must be positive")
        LOG.debug("Use case: User ID validation passed")

        # Verificar que el usuario exista
        LOG.info("Use case: Checking if user exists with ID: %d", user_id)
        existing_user = self.user_repository.get_by_id(user_id)

        if existing_user is None:
            LOG.warning("Use case: DeleteUser - NOT FOUND: User with ID %d not found", user_id)
            raise ValueError(f"User with ID {user_id} not found")

        LOG.info("Use case: User found - Proceeding with deletion")
        LOG.info("  - ID: %s", existing_user.id)
        LOG.info("  - Email: %s", existing_user.email)
        LOG.info("  - Name: %s", existing_user.name)

        # Eliminar usuario del repositorio
        LOG.info("Use case: Calling repository.delete(%d)...", user_id)
        result = self.user_repository.delete(user_id)

        if result:
            LOG.info("Use case: User deleted successfully")
        else:
            LOG.warning("Use case: User deletion returned False (unexpected)")

        LOG.info("-" * 60)
        LOG.info("Use case: DeleteUser - COMPLETED SUCCESSFULLY")
        LOG.info("-" * 60)

        return result
