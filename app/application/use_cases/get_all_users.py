"""
Caso de uso: Obtener Todos los Usuarios.

Contiene la lógica de negocio para obtener una lista de usuarios con paginación.
"""

import logging
from typing import List

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository

LOG = logging.getLogger(__name__)


class GetAllUsersUseCase:
    """
    Caso de uso para obtener todos los usuarios del sistema.

    Responsabilidades:
    - Validar parámetros de paginación
    - Obtener usuarios del repositorio
    - Retornar lista (puede estar vacía)
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa el caso de uso con sus dependencias.

        Args:
            user_repository: Repositorio de usuarios (puerto/interfaz)
        """
        self.user_repository = user_repository

    def execute(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Ejecuta el caso de uso de obtener todos los usuarios.

        Args:
            skip: Número de registros a saltar (para paginación)
            limit: Número máximo de registros a retornar

        Returns:
            List[User]: Lista de usuarios (puede estar vacía)

        Raises:
            ValueError: Si los parámetros de paginación son inválidos
        """
        LOG.info("-" * 60)
        LOG.info("Use case: GetAllUsers - STARTING")
        LOG.info("-" * 60)
        LOG.info("Input parameters:")
        LOG.info("  - skip: %s", skip)
        LOG.info("  - limit: %s", limit)

        # Validación: skip no negativo
        LOG.debug("Use case: Validating skip parameter...")
        if skip < 0:
            LOG.warning(
                "Use case: GetAllUsers - VALIDATION FAILED: Skip must be non-negative: %d", skip
            )
            raise ValueError("Skip must be non-negative")
        LOG.debug("Use case: Skip validation passed")

        # Validación: limit positivo
        LOG.debug("Use case: Validating limit parameter...")
        if limit <= 0:
            LOG.warning(
                "Use case: GetAllUsers - VALIDATION FAILED: Limit must be positive: %d", limit
            )
            raise ValueError("Limit must be positive")
        LOG.debug("Use case: Limit validation passed")

        # Validación: limit máximo 100
        LOG.debug("Use case: Validating limit maximum...")
        if limit > 100:
            LOG.warning(
                "Use case: GetAllUsers - VALIDATION FAILED: Limit cannot exceed 100: %d", limit
            )
            raise ValueError("Limit cannot exceed 100")
        LOG.debug("Use case: Limit maximum validation passed")

        # Obtener usuarios del repositorio
        LOG.info("Use case: Fetching users from repository (skip=%d, limit=%d)...", skip, limit)
        users = self.user_repository.get_all(skip=skip, limit=limit)

        LOG.info("Use case: Users fetched successfully")
        LOG.info("  - Total users returned: %d", len(users))

        if len(users) > 0:
            LOG.debug("Use case: First user: ID=%s, Email=%s", users[0].id, users[0].email)
            if len(users) > 1:
                LOG.debug("Use case: Last user: ID=%s, Email=%s", users[-1].id, users[-1].email)
        else:
            LOG.info("Use case: No users found in the system")

        LOG.info("-" * 60)
        LOG.info("Use case: GetAllUsers - COMPLETED SUCCESSFULLY")
        LOG.info("-" * 60)

        return users
