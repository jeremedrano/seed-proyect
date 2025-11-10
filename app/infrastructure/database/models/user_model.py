"""
Modelo ORM UserModel para SQLAlchemy.

Este modelo representa la tabla 'users' en la base de datos.
NO es parte del dominio, es un detalle de implementación de Infrastructure.
"""
from sqlalchemy import Column, Integer, String
from app.infrastructure.database.models.base import Base


class UserModel(Base):
    """
    Modelo ORM para la tabla 'users'.
    
    Atributos:
        id: Primary key autoincremental
        email: Email único del usuario
        name: Nombre completo del usuario
        age: Edad del usuario
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    
    def __repr__(self) -> str:
        """Representación string del modelo."""
        return f"<UserModel(id={self.id}, email='{self.email}', name='{self.name}', age={self.age})>"

