"""
Schemas Pydantic para User.

Estos schemas se usan para validación HTTP (request/response).
NO son entidades de dominio, son DTOs de la capa de presentación.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateRequest(BaseModel):
    """
    Schema para crear un usuario (request body).
    
    Attributes:
        email: Email válido del usuario
        name: Nombre del usuario (no vacío)
        age: Edad del usuario (positiva)
    """
    email: EmailStr
    name: str = Field(..., min_length=1, description="Nombre del usuario")
    age: int = Field(..., gt=0, description="Edad del usuario (debe ser positiva)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "name": "John Doe",
                    "age": 30
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """
    Schema para respuesta de usuario (response body).
    
    Attributes:
        id: ID del usuario
        email: Email del usuario
        name: Nombre del usuario
        age: Edad del usuario
    """
    id: int
    email: str
    name: str
    age: int
    
    model_config = {
        "from_attributes": True,  # Para compatibilidad con ORM
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "name": "John Doe",
                    "age": 30
                }
            ]
        }
    }


class UserUpdateRequest(BaseModel):
    """
    Schema para actualizar un usuario (request body).
    
    Todos los campos son opcionales para PATCH parcial.
    """
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0)
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Jane Doe",
                    "age": 31
                }
            ]
        }
    }

