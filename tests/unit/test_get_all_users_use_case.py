"""
Tests unitarios para GetAllUsersUseCase.

Valida que el caso de uso de obtener todos los usuarios funcione correctamente.
"""
import pytest
from unittest.mock import Mock
from app.application.use_cases.get_all_users import GetAllUsersUseCase
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_get_all_users_returns_list():
    """Test que obtener todos los usuarios retorna una lista."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    expected_users = [
        User(id=1, email="user1@example.com", name="User 1", age=25),
        User(id=2, email="user2@example.com", name="User 2", age=30),
        User(id=3, email="user3@example.com", name="User 3", age=35),
    ]
    mock_repository.get_all.return_value = expected_users
    
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act
    result = use_case.execute()
    
    # Assert
    mock_repository.get_all.assert_called_once()
    assert result == expected_users
    assert len(result) == 3


@pytest.mark.unit
def test_get_all_users_empty_list():
    """Test que si no hay usuarios, retorna lista vacía."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_all.return_value = []
    
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act
    result = use_case.execute()
    
    # Assert
    mock_repository.get_all.assert_called_once()
    assert result == []
    assert len(result) == 0


@pytest.mark.unit
def test_get_all_users_with_pagination():
    """Test que se pueden paginar los resultados."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    expected_users = [
        User(id=3, email="user3@example.com", name="User 3", age=35),
        User(id=4, email="user4@example.com", name="User 4", age=40),
    ]
    mock_repository.get_all.return_value = expected_users
    
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act
    result = use_case.execute(skip=2, limit=2)
    
    # Assert
    mock_repository.get_all.assert_called_once_with(skip=2, limit=2)
    assert len(result) == 2
    assert result[0].id == 3


@pytest.mark.unit
def test_get_all_users_validates_skip_positive():
    """Test que skip debe ser no negativo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Skip must be non-negative"):
        use_case.execute(skip=-1)
    
    mock_repository.get_all.assert_not_called()


@pytest.mark.unit
def test_get_all_users_validates_limit_positive():
    """Test que limit debe ser positivo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Limit must be positive"):
        use_case.execute(limit=0)
    
    with pytest.raises(ValueError, match="Limit must be positive"):
        use_case.execute(limit=-1)
    
    mock_repository.get_all.assert_not_called()


@pytest.mark.unit
def test_get_all_users_validates_limit_max():
    """Test que limit tiene un máximo de 100."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = GetAllUsersUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Limit cannot exceed 100"):
        use_case.execute(limit=101)
    
    mock_repository.get_all.assert_not_called()

