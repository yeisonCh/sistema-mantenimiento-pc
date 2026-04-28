# app/schemas/activo_ubicacion.py

from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class ActivoUbicacionCrear(BaseModel):
    activo_id: UUID
    ubicacion_id: UUID

class ActivoUbicacionRespuesta(BaseModel):
    id: UUID
    activo_id: UUID
    ubicacion_id: UUID
    fecha_asignacion: datetime
    fecha_retiro: Optional[datetime] = None
    
    class Config:
        from_attributes = True