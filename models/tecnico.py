from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
import uuid

class Tecnico(Base):
    __tablename__ = "tecnicos"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, index=True)
    especialidad = Column(String(100), nullable=True)
    tipo = Column(String(20), nullable=False)  # interno, externo
    persona_id = Column(UNIQUEIDENTIFIER, nullable=False)

    persona = relationship("Persona", foreign_keys=[persona_id], primaryjoin="Tecnico.persona_id == Persona.id")
    empresas = relationship("Empresa", secondary="tecnico_empresa")