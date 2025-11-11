"""
Endpoints REST API para usuarios.

Define los endpoints HTTP para operaciones CRUD de usuarios.
"""
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.application.use_cases.create_user import CreateUserUseCase
from app.application.use_cases.get_user import GetUserUseCase
from app.application.use_cases.get_all_users import GetAllUsersUseCase
from app.presentation.schemas.user_schema import UserCreateRequest, UserResponse, UserListResponse
from app.presentation.api.v1.dependencies import (
    get_create_user_use_case,
    get_get_user_use_case,
    get_get_all_users_use_case
)

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


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un usuario por ID",
    description="Obtiene la información completa de un usuario específico por su ID."
)
def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case)
) -> UserResponse:
    """
    Endpoint para obtener un usuario por su ID.
    
    Args:
        user_id: ID del usuario a buscar
        use_case: Caso de uso GetUser (inyectado)
        
    Returns:
        UserResponse: Usuario encontrado
        
    Raises:
        HTTPException 400: Si el ID es inválido
        HTTPException 404: Si el usuario no existe
    """
    LOG.info("="*60)
    LOG.info("Endpoint: GET /api/v1/users/%d - START", user_id)
    LOG.info("="*60)
    LOG.info("Path parameter:")
    LOG.info("  - user_id: %d", user_id)
    
    try:
        # Ejecutar caso de uso
        LOG.info("Endpoint: Calling GetUserUseCase.execute()...")
        user = use_case.execute(user_id=user_id)
        
        LOG.info("Endpoint: GetUserUseCase completed successfully")
        LOG.info("  - Found user ID: %s", user.id)
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
        LOG.info("Endpoint: GET /api/v1/users/%d - SUCCESS (200)", user_id)
        LOG.info("="*60)
        
        return response
        
    except ValueError as e:
        # Errores de validación del use case
        error_message = str(e)
        LOG.warning("="*60)
        
        if "not found" in error_message.lower():
            LOG.warning("Endpoint: GET /api/v1/users/%d - NOT FOUND", user_id)
            LOG.warning("="*60)
            LOG.warning("User not found: %s", error_message)
            LOG.warning("Returning HTTP 404 Not Found")
            LOG.warning("="*60)
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=error_message
            )
        else:
            LOG.warning("Endpoint: GET /api/v1/users/%d - VALIDATION ERROR", user_id)
            LOG.warning("="*60)
            LOG.warning("Validation error: %s", error_message)
            LOG.warning("Returning HTTP 400 Bad Request")
            LOG.warning("="*60)
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message
            )
    except Exception as e:
        # Errores inesperados
        LOG.error("="*60)
        LOG.error("Endpoint: GET /api/v1/users/%d - INTERNAL ERROR", user_id)
        LOG.error("="*60)
        LOG.error("Unexpected error: %s", str(e), exc_info=True)
        LOG.error("  - user_id: %d", user_id)
        LOG.error("Returning HTTP 500 Internal Server Error")
        LOG.error("="*60)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get(
    "/",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener todos los usuarios",
    description="Obtiene una lista de todos los usuarios con paginación."
)
def get_all_users(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(100, gt=0, le=100, description="Número máximo de registros a retornar"),
    use_case: GetAllUsersUseCase = Depends(get_get_all_users_use_case)
) -> UserListResponse:
    """
    Endpoint para obtener todos los usuarios con paginación.
    
    Args:
        skip: Offset para paginación (default: 0)
        limit: Límite de resultados (default: 100, max: 100)
        use_case: Caso de uso GetAllUsers (inyectado)
        
    Returns:
        UserListResponse: Lista de usuarios con metadatos de paginación
        
    Raises:
        HTTPException 400: Si los parámetros de paginación son inválidos
    """
    LOG.info("="*60)
    LOG.info("Endpoint: GET /api/v1/users/ - START")
    LOG.info("="*60)
    LOG.info("Query parameters:")
    LOG.info("  - skip: %d", skip)
    LOG.info("  - limit: %d", limit)
    
    try:
        # Ejecutar caso de uso
        LOG.info("Endpoint: Calling GetAllUsersUseCase.execute()...")
        users = use_case.execute(skip=skip, limit=limit)
        
        LOG.info("Endpoint: GetAllUsersUseCase completed successfully")
        LOG.info("  - Total users returned: %d", len(users))
        
        # Convertir entidades de dominio a schemas de respuesta
        user_responses = [
            UserResponse(
                id=user.id,
                email=user.email,
                name=user.name,
                age=user.age
            )
            for user in users
        ]
        
        response = UserListResponse(
            users=user_responses,
            total=len(user_responses),
            skip=skip,
            limit=limit
        )
        
        LOG.info("Endpoint: Returning UserListResponse")
        LOG.info("="*60)
        LOG.info("Endpoint: GET /api/v1/users/ - SUCCESS (200)")
        LOG.info("="*60)
        
        return response
        
    except ValueError as e:
        # Errores de validación del use case
        LOG.warning("="*60)
        LOG.warning("Endpoint: GET /api/v1/users/ - VALIDATION ERROR")
        LOG.warning("="*60)
        LOG.warning("Validation error: %s", str(e))
        LOG.warning("  - skip: %d", skip)
        LOG.warning("  - limit: %d", limit)
        LOG.warning("Returning HTTP 400 Bad Request")
        LOG.warning("="*60)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Errores inesperados
        LOG.error("="*60)
        LOG.error("Endpoint: GET /api/v1/users/ - INTERNAL ERROR")
        LOG.error("="*60)
        LOG.error("Unexpected error: %s", str(e), exc_info=True)
        LOG.error("  - skip: %d", skip)
        LOG.error("  - limit: %d", limit)
        LOG.error("Returning HTTP 500 Internal Server Error")
        LOG.error("="*60)
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

