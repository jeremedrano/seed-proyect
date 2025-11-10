"""
Endpoints REST API para usuarios.

Define los endpoints HTTP para operaciones CRUD de usuarios.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.application.use_cases.create_user import CreateUserUseCase
from app.presentation.schemas.user_schema import UserCreateRequest, UserResponse
from app.presentation.api.v1.dependencies import get_create_user_use_case

LOG = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
    description="Crea un nuevo usuario en el sistema con email, nombre y edad."
)
def create_user(
    user_data: UserCreateRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> UserResponse:
    """
    Endpoint para crear un nuevo usuario.
    
    Args:
        user_data: Datos del usuario a crear
        use_case: Caso de uso CreateUser (inyectado)
        
    Returns:
        UserResponse: Usuario creado con ID asignado
        
    Raises:
        HTTPException 400: Si el email ya existe o los datos son inválidos
        HTTPException 422: Si los datos no cumplen con el schema
    """
    LOG.info("Endpoint: POST /users/ - Creating user with email=%s", user_data.email)
    
    try:
        # Ejecutar caso de uso
        user = use_case.execute(
            email=user_data.email,
            name=user_data.name,
            age=user_data.age
        )
        
        LOG.info("Endpoint: POST /users/ - User created with id=%s", user.id)
        
        # Convertir entidad de dominio a schema de respuesta
        return UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            age=user.age
        )
        
    except ValueError as e:
        # Errores de validación del use case
        LOG.warning("Endpoint: POST /users/ - Validation error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Errores inesperados
        LOG.error("Endpoint: POST /users/ - Unexpected error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

