"""
Tests para verificar que la interfaz UserRepository está bien definida.

Estos tests verifican que la interfaz tiene los métodos correctos
usando duck typing (verificamos que cualquier implementación cumpla el contrato).
"""
import pytest
from abc import ABC, abstractmethod
from app.domain.repositories.user_repository import UserRepository
from app.domain.entities.user import User


@pytest.mark.unit
def test_user_repository_is_abstract():
    """Test: UserRepository debe ser una clase abstracta."""
    # Assert
    assert issubclass(UserRepository, ABC)


@pytest.mark.unit
def test_user_repository_has_save_method():
    """Test: UserRepository debe tener método save()."""
    # Assert
    assert hasattr(UserRepository, 'save')
    assert callable(getattr(UserRepository, 'save'))


@pytest.mark.unit
def test_user_repository_has_get_by_id_method():
    """Test: UserRepository debe tener método get_by_id()."""
    # Assert
    assert hasattr(UserRepository, 'get_by_id')
    assert callable(getattr(UserRepository, 'get_by_id'))


@pytest.mark.unit
def test_user_repository_has_get_by_email_method():
    """Test: UserRepository debe tener método get_by_email()."""
    # Assert
    assert hasattr(UserRepository, 'get_by_email')
    assert callable(getattr(UserRepository, 'get_by_email'))


@pytest.mark.unit
def test_user_repository_has_get_all_method():
    """Test: UserRepository debe tener método get_all()."""
    # Assert
    assert hasattr(UserRepository, 'get_all')
    assert callable(getattr(UserRepository, 'get_all'))


@pytest.mark.unit
def test_user_repository_has_update_method():
    """Test: UserRepository debe tener método update()."""
    # Assert
    assert hasattr(UserRepository, 'update')
    assert callable(getattr(UserRepository, 'update'))


@pytest.mark.unit
def test_user_repository_has_delete_method():
    """Test: UserRepository debe tener método delete()."""
    # Assert
    assert hasattr(UserRepository, 'delete')
    assert callable(getattr(UserRepository, 'delete'))


@pytest.mark.unit
def test_cannot_instantiate_user_repository():
    """Test: No se puede instanciar UserRepository directamente (es abstracta)."""
    # Act & Assert
    with pytest.raises(TypeError):
        UserRepository()

