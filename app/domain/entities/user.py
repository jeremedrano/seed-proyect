"""
Entidad User del dominio.

Esta es la entidad principal del dominio, representa un usuario del sistema.
NO tiene dependencias de frameworks o librerías externas.
Solo contiene lógica de negocio pura.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    Entidad User con lógica de negocio pura.
    
    Attributes:
        id: Identificador único del usuario (None si es nuevo)
        email: Email del usuario
        name: Nombre completo del usuario
        age: Edad del usuario en años
    """
    id: Optional[int]
    email: str
    name: str
    age: int
    
    def is_adult(self) -> bool:
        """
        Determina si el usuario es mayor de edad.
        
        Returns:
            bool: True si el usuario tiene 18 años o más, False en caso contrario.
        """
        return self.age >= 18

