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
    LOG.info("="*60)
    LOG.info("Endpoint: POST /api/v1/users/ - START")
    LOG.info("="*60)
    LOG.info("Request data:")
    LOG.info("  - Email: %s", user_data.email)
    LOG.info("  - Name: %s", user_data.name)
    LOG.info("  - Age: %s", user_data.age)
    
    try:
        # Ejecutar caso de uso
        LOG.info("Endpoint: Calling CreateUserUseCase.execute()...")
        user = use_case.execute(
            email=user_data.email,
            name=user_data.name,
            age=user_data.age
        )
        
        LOG.info("Endpoint: CreateUserUseCase completed successfully")
        LOG.info("  - Created user ID: %s", user.id)
        LOG.info("  - Email: %s", user.email)
        LOG.info("  - Name: %s", user.name)
        LOG.info("  - Age: %s", user.age)
        
        # Convertir entidad de dominio a schema de respuesta
        response = UserResponse(
            id=user.id,
            email=user.email,
            name=user.name,
            age=user.age
        )
        
        LOG.info("Endpoint: Returning UserResponse")
        LOG.info("="*60)
        LOG.info("Endpoint: POST /api/v1/users/ - SUCCESS (201)")
        LOG.info("="*60)
        
        return response
        
    except ValueError as e:
        # Errores de validación del use case
        LOG.warning("="*60)
        LOG.warning("Endpoint: POST /api/v1/users/ - VALIDATION ERROR")
        LOG.warning("="*60)
        LOG.warning("Validation error: %s", str(e))
        LOG.warning("  - Email: %s", user_data.email)
        LOG.warning("  - Name: %s", user_data.name)
        LOG.warning("  - Age: %s", user_data.age)
        LOG.warning("Returning HTTP 400 Bad Request")
        LOG.warning("="*60)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Errores inesperados
        LOG.error("="*60)
        LOG.error("Endpoint: POST /api/v1/users/ - INTERNAL ERROR")
        LOG.error("="*60)
        LOG.error("Unexpected error: %s", str(e), exc_info=True)
        LOG.error("  - Email: %s", user_data.email)
        LOG.error("  - Name: %s", user_data.name)
        LOG.error("  - Age: %s", user_data.age)
        LOG.error("Returning HTTP 500 Internal Server Error")
        LOG.error("="*60)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

