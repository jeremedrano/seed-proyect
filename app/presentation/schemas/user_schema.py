"""
Schemas Pydantic para User.

Estos schemas se usan para validación HTTP (request/response).
NO son entidades de dominio, son DTOs de la capa de presentación.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List


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


class UserListResponse(BaseModel):
    """
    Schema para respuesta de lista de usuarios con metadatos de paginación.
    
    Attributes:
        users: Lista de usuarios
        total: Número total de usuarios retornados
        skip: Offset usado en la paginación
        limit: Límite usado en la paginación
    """
    users: List[UserResponse]
    total: int = Field(..., description="Número de usuarios en esta página")
    skip: int = Field(..., description="Offset de paginación")
    limit: int = Field(..., description="Límite de paginación")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "users": [
                        {
                            "id": 1,
                            "email": "user1@example.com",
                            "name": "User 1",
                            "age": 25
                        },
                        {
                            "id": 2,
                            "email": "user2@example.com",
                            "name": "User 2",
                            "age": 30
                        }
                    ],
                    "total": 2,
                    "skip": 0,
                    "limit": 100
                }
            ]
        }
    }

