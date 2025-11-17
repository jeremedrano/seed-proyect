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
        LOG.info("-" * 60)
        LOG.info("Use case: CreateUser - STARTING")
        LOG.info("-" * 60)
        LOG.info("Input parameters:")
        LOG.info("  - email: %s", email)
        LOG.info("  - name: %s", name)
        LOG.info("  - age: %s", age)

        # Validación: nombre no vacío
        LOG.debug("Use case: Validating name...")
        if not name or name.strip() == "":
            LOG.warning("Use case: CreateUser - VALIDATION FAILED: Name is empty")
            raise ValueError("Name cannot be empty")
        LOG.debug("Use case: Name validation passed")

        # Validación: formato de email
        LOG.debug("Use case: Validating email format...")
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, email):
            LOG.warning("Use case: CreateUser - VALIDATION FAILED: Invalid email format: %s", email)
            raise ValueError("Invalid email format")
        LOG.debug("Use case: Email format validation passed")

        # Validación: edad positiva
        LOG.debug("Use case: Validating age...")
        if age <= 0:
            LOG.warning("Use case: CreateUser - VALIDATION FAILED: Age must be positive: %d", age)
            raise ValueError("Age must be positive")
        LOG.debug("Use case: Age validation passed")

        # Verificar que el email no exista
        LOG.info("Use case: Checking if email already exists...")
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            LOG.warning("Use case: CreateUser - VALIDATION FAILED: Email already exists: %s", email)
            LOG.warning("  - Existing user ID: %s", existing_user.id)
            raise ValueError("Email already exists")
        LOG.info("Use case: Email is available (not in use)")

        # Crear entidad User (sin ID)
        LOG.info("Use case: Creating User entity...")
        user = User(id=None, email=email, name=name, age=age)
        LOG.info("Use case: User entity created successfully")
        LOG.debug("  - User entity: %s", user)

        # Guardar en repositorio
        LOG.info("Use case: Calling repository.save()...")
        saved_user = self.user_repository.save(user)
        LOG.info("Use case: User saved successfully in repository")
        LOG.info("  - Assigned ID: %s", saved_user.id)
        LOG.info("  - Email: %s", saved_user.email)
        LOG.info("  - Name: %s", saved_user.name)
        LOG.info("  - Age: %s", saved_user.age)

        LOG.info("-" * 60)
        LOG.info("Use case: CreateUser - COMPLETED SUCCESSFULLY")
        LOG.info("-" * 60)

        return saved_user
