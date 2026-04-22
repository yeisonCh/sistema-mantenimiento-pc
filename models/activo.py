from database import Base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
import uuid

class Activo(Base):
    __tablename__ = "activos"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    serial = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(100), nullable=True)
    marca = Column(String(50), nullable=True)
    modelo = Column(String(50), nullable=True)
    fecha_compra = Column(Date, nullable=True)
    estado = Column(String(50), nullable=False)  # activo, dañado, en_mantenimiento, baja

    tipo_activo_id = Column(UNIQUEIDENTIFIER, ForeignKey("tipo_activo.id"), nullable=False)
    empresa_id = Column(UNIQUEIDENTIFIER, ForeignKey("empresas.id"), nullable=False)
    usuario_responsable_id = Column(UNIQUEIDENTIFIER, ForeignKey("usuarios.id"), nullable=True)

    tipo_activo = relationship("TipoActivo")
    empresa = relationship("Empresa")
    usuario_responsable = relationship("Usuario")