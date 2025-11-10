"""
Tests unitarios para el caso de uso CreateUser.

Usa mocks del repositorio para testear la lógica sin depender de DB real.
"""
import pytest
from unittest.mock import Mock
from app.application.use_cases.create_user import CreateUserUseCase
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_create_user_calls_repository_save():
    """Test: CreateUser debe llamar al método save() del repositorio."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_email.return_value = None  # Email no existe
    mock_repository.save.return_value = User(
        id=1,
        email="test@example.com",
        name="Test User",
        age=25
    )
    use_case = CreateUserUseCase(mock_repository)
    
    # Act
    result = use_case.execute(
        email="test@example.com",
        name="Test User",
        age=25
    )
    
    # Assert
    mock_repository.save.assert_called_once()
    assert result.id == 1
    assert result.email == "test@example.com"


@pytest.mark.unit
def test_create_user_with_existing_email():
    """Test: No se puede crear usuario con email existente."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_email.return_value = User(
        id=1,
        email="existing@example.com",
        name="Existing User",
        age=30
    )
    use_case = CreateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Email already exists"):
        use_case.execute(
            email="existing@example.com",
            name="New User",
            age=25
        )
    
    # Verificar que NO se llamó a save()
    mock_repository.save.assert_not_called()


@pytest.mark.unit
def test_create_user_validates_age():
    """Test: La edad debe ser un número positivo."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_email.return_value = None
    use_case = CreateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Age must be positive"):
        use_case.execute(
            email="test@example.com",
            name="Test User",
            age=-5
        )
    
    mock_repository.save.assert_not_called()


@pytest.mark.unit
def test_create_user_validates_email_format():
    """Test: El email debe tener formato válido."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_email.return_value = None
    use_case = CreateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Invalid email format"):
        use_case.execute(
            email="invalid-email",
            name="Test User",
            age=25
        )
    
    mock_repository.save.assert_not_called()


@pytest.mark.unit
def test_create_user_validates_name_not_empty():
    """Test: El nombre no puede estar vacío."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    mock_repository.get_by_email.return_value = None
    use_case = CreateUserUseCase(mock_repository)
    
    # Act & Assert
    with pytest.raises(ValueError, match="Name cannot be empty"):
        use_case.execute(
            email="test@example.com",
            name="",
            age=25
        )
    
    mock_repository.save.assert_not_called()


@pytest.mark.unit
def test_create_user_creates_user_with_none_id():
    """Test: El usuario creado debe tener id=None antes de guardar."""
    # Arrange
    mock_repository = Mock(spec=UserRepository)
    saved_user = User(id=1, email="test@example.com", name="Test", age=25)
    mock_repository.save.return_value = saved_user
    mock_repository.get_by_email.return_value = None
    use_case = CreateUserUseCase(mock_repository)
    
    # Act
    use_case.execute(email="test@example.com", name="Test", age=25)
    
    # Assert - Verificar que se llamó con User(id=None)
    call_args = mock_repository.save.call_args[0][0]
    assert call_args.id is None
    assert call_args.email == "test@example.com"
    assert call_args.name == "Test"
    assert call_args.age == 25

