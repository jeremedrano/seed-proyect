"""
Interfaz UserRepository (Puerto en Arquitectura Hexagonal).

Define el contrato que debe cumplir cualquier implementación de repositorio.
Esta interfaz está en Domain y NO depende de frameworks o implementaciones.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.user import User


class UserRepository(ABC):
    """
    Interfaz abstracta para el repositorio de usuarios.
    
    Define las operaciones CRUD que cualquier implementación debe proveer.
    Los adaptadores (Infrastructure) implementarán esta interfaz.
    """
    
    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guarda un usuario nuevo en el sistema.
        
        Args:
            user: Usuario a guardar (con id=None)
            
        Returns:
            User: Usuario guardado con ID asignado
        """
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtiene un usuario por su email.
        
        Args:
            email: Email del usuario a buscar
            
        Returns:
            Optional[User]: Usuario encontrado o None si no existe
        """
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Obtiene todos los usuarios del sistema con paginación.
        
        Args:
            skip: Número de registros a saltar (default: 0)
            limit: Número máximo de registros a retornar (default: 100)
        
        Returns:
            List[User]: Lista de usuarios (vacía si no hay usuarios)
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por su ID.
        
        Args:
            user_id: ID del usuario a eliminar
            
        Returns:
            bool: True si fue eliminado, False si no existía
        """
        pass

