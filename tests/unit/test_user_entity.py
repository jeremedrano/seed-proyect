"""
Tests unitarios para la entidad User del dominio.

Estos tests verifican la lógica de negocio de la entidad User
sin dependencias externas (no DB, no frameworks).
"""
import pytest
from app.domain.entities.user import User


@pytest.mark.unit
def test_user_creation():
    """Test: Crear una instancia de User con todos los campos."""
    # Arrange & Act
    user = User(
        id=1,
        email="test@example.com",
        name="Test User",
        age=25
    )
    
    # Assert
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.age == 25


@pytest.mark.unit
def test_user_creation_without_id():
    """Test: Crear un User sin ID (para casos de creación nueva)."""
    # Arrange & Act
    user = User(
        id=None,
        email="newuser@example.com",
        name="New User",
        age=30
    )
    
    # Assert
    assert user.id is None
    assert user.email == "newuser@example.com"


@pytest.mark.unit
def test_user_is_adult():
    """Test: Verificar si un usuario es adulto (>= 18 años)."""
    # Arrange
    adult_user = User(id=1, email="adult@example.com", name="Adult", age=20)
    minor_user = User(id=2, email="minor@example.com", name="Minor", age=15)
    
    # Act & Assert
    assert adult_user.is_adult() is True
    assert minor_user.is_adult() is False


@pytest.mark.unit
def test_user_is_adult_edge_case():
    """Test: Usuario con exactamente 18 años es adulto."""
    # Arrange
    user = User(id=1, email="eighteen@example.com", name="Eighteen", age=18)
    
    # Act & Assert
    assert user.is_adult() is True

