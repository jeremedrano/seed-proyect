"""
Tests de integración para UserRepositoryImpl.

Estos tests usan una base de datos real (SQLite en memoria)
para verificar que el repositorio funciona correctamente.
"""
import pytest
from app.domain.entities.user import User
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl


@pytest.mark.integration
def test_save_user_assigns_id(db_session):
    """Test: Guardar un usuario asigna un ID automáticamente."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="test@example.com", name="Test User", age=25)
    
    # Act
    saved_user = repository.save(user)
    
    # Assert
    assert saved_user.id is not None
    assert saved_user.id > 0
    assert saved_user.email == "test@example.com"
    assert saved_user.name == "Test User"
    assert saved_user.age == 25


@pytest.mark.integration
def test_get_by_id_returns_user(db_session):
    """Test: Obtener usuario por ID retorna el usuario correcto."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="test@example.com", name="Test User", age=25)
    saved_user = repository.save(user)
    
    # Act
    found_user = repository.get_by_id(saved_user.id)
    
    # Assert
    assert found_user is not None
    assert found_user.id == saved_user.id
    assert found_user.email == saved_user.email


@pytest.mark.integration
def test_get_by_id_returns_none_when_not_found(db_session):
    """Test: Obtener usuario inexistente retorna None."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    
    # Act
    found_user = repository.get_by_id(999)
    
    # Assert
    assert found_user is None


@pytest.mark.integration
def test_get_by_email_returns_user(db_session):
    """Test: Obtener usuario por email funciona correctamente."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="unique@example.com", name="Unique", age=30)
    repository.save(user)
    
    # Act
    found_user = repository.get_by_email("unique@example.com")
    
    # Assert
    assert found_user is not None
    assert found_user.email == "unique@example.com"
    assert found_user.name == "Unique"


@pytest.mark.integration
def test_get_by_email_returns_none_when_not_found(db_session):
    """Test: Buscar email inexistente retorna None."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    
    # Act
    found_user = repository.get_by_email("notfound@example.com")
    
    # Assert
    assert found_user is None


@pytest.mark.integration
def test_get_all_returns_all_users(db_session, sample_users_data):
    """Test: get_all retorna todos los usuarios."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    for user_data in sample_users_data:
        user = User(id=None, **user_data)
        repository.save(user)
    
    # Act
    all_users = repository.get_all()
    
    # Assert
    assert len(all_users) == 3
    assert all(isinstance(user, User) for user in all_users)
    emails = [user.email for user in all_users]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails
    assert "user3@example.com" in emails


@pytest.mark.integration
def test_get_all_returns_empty_list_when_no_users(db_session):
    """Test: get_all retorna lista vacía si no hay usuarios."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    
    # Act
    all_users = repository.get_all()
    
    # Assert
    assert all_users == []


@pytest.mark.integration
def test_update_user_modifies_data(db_session):
    """Test: Actualizar usuario modifica los datos correctamente."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="old@example.com", name="Old Name", age=25)
    saved_user = repository.save(user)
    
    # Modificar datos
    saved_user.name = "New Name"
    saved_user.age = 30
    
    # Act
    updated_user = repository.update(saved_user)
    
    # Assert
    assert updated_user.id == saved_user.id
    assert updated_user.name == "New Name"
    assert updated_user.age == 30
    
    # Verificar en DB
    found_user = repository.get_by_id(saved_user.id)
    assert found_user.name == "New Name"
    assert found_user.age == 30


@pytest.mark.integration
def test_update_user_without_id_raises_error(db_session):
    """Test: Actualizar usuario sin ID lanza error."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="test@example.com", name="Test", age=25)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User must have an ID"):
        repository.update(user)


@pytest.mark.integration
def test_update_nonexistent_user_raises_error(db_session):
    """Test: Actualizar usuario inexistente lanza error."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=999, email="test@example.com", name="Test", age=25)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User with id 999 not found"):
        repository.update(user)


@pytest.mark.integration
def test_delete_user_removes_from_db(db_session):
    """Test: Eliminar usuario lo remueve de la DB."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    user = User(id=None, email="delete@example.com", name="Delete Me", age=25)
    saved_user = repository.save(user)
    
    # Act
    result = repository.delete(saved_user.id)
    
    # Assert
    assert result is True
    
    # Verificar que ya no existe
    found_user = repository.get_by_id(saved_user.id)
    assert found_user is None


@pytest.mark.integration
def test_delete_nonexistent_user_returns_false(db_session):
    """Test: Eliminar usuario inexistente retorna False."""
    # Arrange
    repository = UserRepositoryImpl(db_session)
    
    # Act
    result = repository.delete(999)
    
    # Assert
    assert result is False

