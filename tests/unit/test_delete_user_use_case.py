"""
Tests unitarios para DeleteUserUseCase.

Valida que el caso de uso de eliminar un usuario funcione correctamente.
"""
import pytest
from unittest.mock import Mock
from app.application.use_cases.delete_user import DeleteUserUseCase
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_delete_user_deletes_existing_user():
    """Test que eliminar un usuario existente retorna True."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="User", age=25)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.delete.return_value = True
    
    use_case = DeleteUserUseCase(mock_repository)
    
    # Act
    result = use_case.execute(user_id=1)
    
    # Assert
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.delete.assert_called_once_with(1)
    assert result is True


@pytest.mark.unit
def test_delete_user_not_found_raises_error():
    """Test que eliminar un usuario inexistente lanza ValueError."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_id.return_value = None
    
    use_case = DeleteUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User with ID 999 not found"):
        use_case.execute(user_id=999)
    
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.delete.assert_not_called()


@pytest.mark.unit
def test_delete_user_validates_positive_id():
    """Test que se valida que el ID sea positivo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = DeleteUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=0)
    
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=-1)
    
    mock_repository.get_by_id.assert_not_called()
    mock_repository.delete.assert_not_called()


@pytest.mark.unit
def test_delete_user_calls_repository_delete():
    """Test que se llama al método delete del repositorio con el ID correcto."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=5, email="test@example.com", name="Test", age=30)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.delete.return_value = True
    
    use_case = DeleteUserUseCase(mock_repository)
    
    # Act
    result = use_case.execute(user_id=5)
    
    # Assert
    mock_repository.delete.assert_called_once_with(5)
    assert result is True

