from database import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class TipoActivo(Base):
    __tablename__ = "tipo_activo"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String(50), nullable=False, unique=True)