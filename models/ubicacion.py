from database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class Ubicacion(Base):
    __tablename__ = "ubicaciones"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200), nullable=True)
    empresa_id = Column(UNIQUEIDENTIFIER, nullable=True)