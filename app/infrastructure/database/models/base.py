"""
Base declarativa para modelos SQLAlchemy.

Todos los modelos ORM deben heredar de esta clase Base.
"""

from sqlalchemy.orm import declarative_base

# Base declarativa para todos los modelos
Base = declarative_base()
