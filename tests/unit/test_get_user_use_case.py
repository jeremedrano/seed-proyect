"""
Tests unitarios para GetUserUseCase.

Valida que el caso de uso de obtener un usuario funcione correctamente.
"""
import pytest
from unittest.mock import Mock
from app.application.use_cases.get_user import GetUserUseCase
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_get_user_by_id_returns_user():
    """Test que obtener un usuario por ID retorna el usuario correcto."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    expected_user = User(id=1, email="test@example.com", name="Test User", age=25)
    mock_repository.get_by_id.return_value = expected_user
    
    use_case = GetUserUseCase(mock_repository)
    
    # Act
    result = use_case.execute(user_id=1)
    
    # Assert
    mock_repository.get_by_id.assert_called_once_with(1)
    assert result == expected_user
    assert result.id == 1
    assert result.email == "test@example.com"


@pytest.mark.unit
def test_get_user_by_id_not_found_raises_error():
    """Test que obtener un usuario inexistente lanza ValueError."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_id.return_value = None
    
    use_case = GetUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User with ID 999 not found"):
        use_case.execute(user_id=999)
    
    mock_repository.get_by_id.assert_called_once_with(999)


@pytest.mark.unit
def test_get_user_validates_positive_id():
    """Test que se valida que el ID sea positivo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = GetUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=0)
    
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=-1)
    
    # No debe llamar al repositorio si la validación falla
    mock_repository.get_by_id.assert_not_called()

