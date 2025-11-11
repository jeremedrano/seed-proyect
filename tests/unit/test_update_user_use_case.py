"""
Tests unitarios para UpdateUserUseCase.

Valida que el caso de uso de actualizar un usuario funcione correctamente.
"""
import pytest
from unittest.mock import Mock
from app.application.use_cases.update_user import UpdateUserUseCase
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_update_user_updates_all_fields():
    """Test que actualizar un usuario modifica todos los campos."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="old@example.com", name="Old Name", age=25)
    updated_user = User(id=1, email="new@example.com", name="New Name", age=30)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = None  # Email nuevo disponible
    mock_repository.update.return_value = updated_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act
    result = use_case.execute(
        user_id=1,
        email="new@example.com",
        name="New Name",
        age=30
    )
    
    # Assert
    mock_repository.get_by_id.assert_called_once_with(1)
    mock_repository.update.assert_called_once()
    assert result.email == "new@example.com"
    assert result.name == "New Name"
    assert result.age == 30


@pytest.mark.unit
def test_update_user_partial_update():
    """Test que se puede actualizar solo algunos campos."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="Old Name", age=25)
    updated_user = User(id=1, email="user@example.com", name="New Name", age=25)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.update.return_value = updated_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act - Solo actualizar nombre
    result = use_case.execute(user_id=1, name="New Name")
    
    # Assert
    mock_repository.update.assert_called_once()
    assert result.name == "New Name"
    # Email y age deberían permanecer igual
    assert result.email == "user@example.com"
    assert result.age == 25


@pytest.mark.unit
def test_update_user_not_found_raises_error():
    """Test que actualizar un usuario inexistente lanza ValueError."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_id.return_value = None
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User with ID 999 not found"):
        use_case.execute(user_id=999, name="New Name")
    
    mock_repository.get_by_id.assert_called_once_with(999)
    mock_repository.update.assert_not_called()


@pytest.mark.unit
def test_update_user_validates_positive_id():
    """Test que se valida que el ID sea positivo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=0, name="Test")
    
    with pytest.raises(ValueError, match="User ID must be positive"):
        use_case.execute(user_id=-1, name="Test")
    
    mock_repository.get_by_id.assert_not_called()


@pytest.mark.unit
def test_update_user_validates_email_format():
    """Test que se valida el formato del email si se proporciona."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="User", age=25)
    mock_repository.get_by_id.return_value = existing_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email format"):
        use_case.execute(user_id=1, email="invalid-email")
    
    mock_repository.update.assert_not_called()


@pytest.mark.unit
def test_update_user_validates_name_not_empty():
    """Test que el nombre no puede estar vacío si se proporciona."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="User", age=25)
    mock_repository.get_by_id.return_value = existing_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Name cannot be empty"):
        use_case.execute(user_id=1, name="")
    
    with pytest.raises(ValueError, match="Name cannot be empty"):
        use_case.execute(user_id=1, name="   ")
    
    mock_repository.update.assert_not_called()


@pytest.mark.unit
def test_update_user_validates_age_positive():
    """Test que la edad debe ser positiva si se proporciona."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="User", age=25)
    mock_repository.get_by_id.return_value = existing_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Age must be positive"):
        use_case.execute(user_id=1, age=0)
    
    with pytest.raises(ValueError, match="Age must be positive"):
        use_case.execute(user_id=1, age=-5)
    
    mock_repository.update.assert_not_called()


@pytest.mark.unit
def test_update_user_email_already_exists_for_another_user():
    """Test que no se puede cambiar a un email que ya usa otro usuario."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user1@example.com", name="User 1", age=25)
    other_user = User(id=2, email="user2@example.com", name="User 2", age=30)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = other_user  # Email ya existe en otro usuario
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(user_id=1, email="user2@example.com")
    
    mock_repository.update.assert_not_called()


@pytest.mark.unit
def test_update_user_can_keep_same_email():
    """Test que se puede mantener el mismo email (no es conflicto)."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="Old Name", age=25)
    updated_user = User(id=1, email="user@example.com", name="New Name", age=25)
    
    mock_repository.get_by_id.return_value = existing_user
    mock_repository.get_by_email.return_value = existing_user  # Mismo usuario
    mock_repository.update.return_value = updated_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act - Actualizar nombre pero mantener email
    result = use_case.execute(user_id=1, email="user@example.com", name="New Name")
    
    # Assert
    mock_repository.update.assert_called_once()
    assert result.name == "New Name"


@pytest.mark.unit
def test_update_user_requires_at_least_one_field():
    """Test que se requiere actualizar al menos un campo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    existing_user = User(id=1, email="user@example.com", name="User", age=25)
    mock_repository.get_by_id.return_value = existing_user
    
    use_case = UpdateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="At least one field must be provided for update"):
        use_case.execute(user_id=1)  # Sin ningún campo
    
    mock_repository.update.assert_not_called()

