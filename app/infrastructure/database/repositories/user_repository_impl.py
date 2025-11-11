"""
Implementación del repositorio de usuarios usando SQLAlchemy.

Este adaptador implementa la interfaz UserRepository (puerto del dominio)
usando SQLAlchemy como tecnología de persistencia.
"""
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel

LOG = logging.getLogger(__name__)


class UserRepositoryImpl(UserRepository):
    """
    Implementación del repositorio de usuarios con SQLAlchemy.
    
    Adaptador que traduce entre:
    - User (entidad del dominio)
    - UserModel (modelo ORM)
    """
    
    def __init__(self, session: Session):
        """
        Inicializa el repositorio con una sesión de SQLAlchemy.
        
        Args:
            session: Sesión de SQLAlchemy para operaciones de DB
        """
        self.session = session
    
    def save(self, user: User) -> User:
        """
        Guarda un usuario nuevo en la base de datos.
        
        Args:
            user: Usuario a guardar (con id=None)
            
        Returns:
            User: Usuario guardado con ID asignado
        """
        LOG.info("." * 60)
        LOG.info("Repository: save() - STARTING")
        LOG.info("." * 60)
        LOG.info("User data to save:")
        LOG.info("  - ID: %s (should be None)", user.id)
        LOG.info("  - Email: %s", user.email)
        LOG.info("  - Name: %s", user.name)
        LOG.info("  - Age: %s", user.age)
        
        # Convertir entidad de dominio a modelo ORM
        LOG.info("Repository: Converting domain entity to ORM model...")
        user_model = UserModel(
            email=user.email,
            name=user.name,
            age=user.age
        )
        LOG.debug("Repository: UserModel created: %s", user_model)
        
        # Guardar en DB
        LOG.info("Repository: Adding UserModel to session...")
        self.session.add(user_model)
        LOG.info("Repository: Committing transaction...")
        self.session.commit()
        LOG.info("Repository: Transaction committed successfully")
        LOG.info("Repository: Refreshing UserModel from DB...")
        self.session.refresh(user_model)
        LOG.info("Repository: User saved successfully in database")
        LOG.info("  - Assigned ID: %s", user_model.id)
        LOG.info("  - Email: %s", user_model.email)
        
        # Convertir modelo ORM de vuelta a entidad de dominio
        LOG.info("Repository: Converting ORM model back to domain entity...")
        result = self._to_entity(user_model)
        LOG.info("." * 60)
        LOG.info("Repository: save() - COMPLETED SUCCESSFULLY")
        LOG.info("." * 60)
        
        return result
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        LOG.debug("Repository: Getting user by id=%s", user_id)
        
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        
        if user_model is None:
            LOG.debug("Repository: User with id=%s not found", user_id)
            return None
        
        LOG.debug("Repository: User with id=%s found", user_id)
        return self._to_entity(user_model)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        LOG.info("Repository: get_by_email() - Searching for email: %s", email)
        
        LOG.debug("Repository: Executing query: SELECT * FROM users WHERE email = '%s'", email)
        user_model = self.session.query(UserModel).filter(
            UserModel.email == email
        ).first()
        
        if user_model is None:
            LOG.info("Repository: get_by_email() - No user found with email: %s", email)
            return None
        
        LOG.info("Repository: get_by_email() - User found!")
        LOG.info("  - ID: %s", user_model.id)
        LOG.info("  - Email: %s", user_model.email)
        LOG.info("  - Name: %s", user_model.name)
        LOG.info("  - Age: %s", user_model.age)
        return self._to_entity(user_model)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Obtiene todos los usuarios del sistema con paginación.
        
        Args:
            skip: Número de registros a saltar (default: 0)
            limit: Número máximo de registros a retornar (default: 100)
        
        Returns:
            List[User]: Lista de usuarios (vacía si no hay usuarios)
        """
        LOG.info("Repository: get_all() - Fetching users (skip=%d, limit=%d)", skip, limit)
        
        user_models = self.session.query(UserModel).offset(skip).limit(limit).all()
        
        LOG.info("Repository: get_all() - Found %d users", len(user_models))
        
        return [self._to_entity(model) for model in user_models]
    
    def update(self, user: User) -> User:
        """
        Actualiza un usuario existente.
        
        Args:
            user: Usuario con datos actualizados (debe tener ID)
            
        Returns:
            User: Usuario actualizado
            
        Raises:
            ValueError: Si el usuario no tiene ID o no existe
        """
        LOG.info("Repository: Updating user with id=%s", user.id)
        
        if user.id is None:
            LOG.error("Repository: Cannot update user without ID")
            raise ValueError("User must have an ID to be updated")
        
        # Buscar usuario existente
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user.id
        ).first()
        
        if user_model is None:
            LOG.error("Repository: User with id=%s not found for update", user.id)
            raise ValueError(f"User with id {user.id} not found")
        
        # Actualizar campos
        user_model.email = user.email
        user_model.name = user.name
        user_model.age = user.age
        
        # Guardar cambios
        self.session.commit()
        self.session.refresh(user_model)
        
        LOG.info("Repository: User with id=%s updated", user.id)
        
        return self._to_entity(user_model)
    
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por su ID.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            bool: True si fue eliminado, False si no existía
        """
        LOG.info("Repository: Deleting user with id=%s", user_id)
        
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()
        
        if user_model is None:
            LOG.warning("Repository: User with id=%s not found for deletion", user_id)
            return False
        
        self.session.delete(user_model)
        self.session.commit()
        
        LOG.info("Repository: User with id=%s deleted", user_id)
        return True
    
    def _to_entity(self, user_model: UserModel) -> User:
        """
        Convierte un UserModel (ORM) a User (entidad de dominio).
        
        Args:
            user_model: Modelo ORM de SQLAlchemy
            
        Returns:
            User: Entidad de dominio
        """
        return User(
            id=user_model.id,
            email=user_model.email,
            name=user_model.name,
            age=user_model.age
        )

