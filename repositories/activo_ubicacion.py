# app/repositories/activo_ubicacion.py

from datetime import datetime

from sqlalchemy.orm import Session
from models.activo_ubicacion import ActivoUbicacion
from schemas.activo_ubicacion import ActivoUbicacionCrear
from uuid import UUID
from typing import List

def obtener_historial_por_activo(db: Session, activo_id: UUID) -> List[ActivoUbicacion]:
    return db.query(ActivoUbicacion).filter(ActivoUbicacion.activo_id == activo_id).order_by(ActivoUbicacion.fecha_asignacion.desc()).all()

def obtener_ubicacion_actual(db: Session, activo_id: UUID):
    return db.query(ActivoUbicacion).filter(
        ActivoUbicacion.activo_id == activo_id,
        ActivoUbicacion.fecha_retiro.is_(None)
    ).first()

def crear_movimiento(db: Session, movimiento: ActivoUbicacionCrear) -> ActivoUbicacion:
    nuevo = ActivoUbicacion(
        activo_id=movimiento.activo_id,
        ubicacion_id=movimiento.ubicacion_id
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def retirar_ubicacion_actual(db: Session, activo_id: UUID) -> bool:
    actual = obtener_ubicacion_actual(db, activo_id)
    if actual:
        actual.fecha_retiro = datetime.now()
        db.commit()
        return True
    return False