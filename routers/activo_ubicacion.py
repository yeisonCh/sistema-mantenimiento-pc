# app/routers/activo_ubicacion.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from database import get_db
from schemas.activo_ubicacion import ActivoUbicacionCrear, ActivoUbicacionRespuesta
from repositories.activo_ubicacion import (
    obtener_historial_por_activo,
    obtener_ubicacion_actual,
    crear_movimiento,
    retirar_ubicacion_actual
)

router = APIRouter(prefix="/activos-ubicaciones", tags=["Activos Ubicaciones"])

@router.get("/historial/{activo_id}", response_model=list[ActivoUbicacionRespuesta])
def historial_activo(activo_id: UUID, db: Session = Depends(get_db)):
    return obtener_historial_por_activo(db, activo_id)

@router.get("/actual/{activo_id}", response_model=ActivoUbicacionRespuesta)
def ubicacion_actual(activo_id: UUID, db: Session = Depends(get_db)):
    ubicacion = obtener_ubicacion_actual(db, activo_id)
    if not ubicacion:
        raise HTTPException(404, "Activo sin ubicación asignada")
    return ubicacion

@router.post("/mover", response_model=ActivoUbicacionRespuesta, status_code=201)
def mover_activo(movimiento: ActivoUbicacionCrear, db: Session = Depends(get_db)):
    retirar_ubicacion_actual(db, movimiento.activo_id)
    return crear_movimiento(db, movimiento)