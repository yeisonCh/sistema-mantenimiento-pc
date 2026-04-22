from database import Base
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
import uuid

class ActivoRelacion(Base):
    __tablename__ = "activo_relacion"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_asignacion = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    motivo_retiro = Column(String(200), nullable=True)

    activo_padre_id = Column(UNIQUEIDENTIFIER, ForeignKey("activos.id"), nullable=False)
    activo_hijo_id = Column(UNIQUEIDENTIFIER, ForeignKey("activos.id"), nullable=False)

    activo_padre = relationship("Activo", foreign_keys=[activo_padre_id])
    activo_hijo = relationship("Activo", foreign_keys=[activo_hijo_id])