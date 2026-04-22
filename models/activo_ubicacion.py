from database import Base
from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
import uuid

class ActivoUbicacion(Base):
    __tablename__ = "activo_ubicacion"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)

    activo_id = Column(UNIQUEIDENTIFIER, ForeignKey("activos.id"), nullable=False)
    ubicacion_id = Column(UNIQUEIDENTIFIER, ForeignKey("ubicaciones.id"), nullable=False)

    activo = relationship("Activo")
    ubicacion = relationship("Ubicacion")