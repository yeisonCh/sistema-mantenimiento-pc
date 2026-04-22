from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class TecnicoEmpresa(Base):
    __tablename__ = "tecnico_empresa"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    tecnico_id = Column(UNIQUEIDENTIFIER, nullable=False)
    empresa_id = Column(UNIQUEIDENTIFIER, nullable=False)