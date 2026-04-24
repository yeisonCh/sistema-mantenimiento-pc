# app/routers/persona.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import get_db
from schemas.persona import PersonaCrear, PersonaActualizar, PersonaRespuesta
from services.persona import (
    service_obtener_personas,
    service_obtener_persona_por_id,
    service_crear_persona,
    service_actualizar_persona,
    service_eliminar_persona
)

router = APIRouter(
    prefix="/personas",
    tags=["Personas"]
)

# GET: /personas
@router.get(
    "/", 
    response_model=List[PersonaRespuesta],
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las personas",
    description="Retorna una lista con todas las personas registradas"
)
def listar_personas(db: Session = Depends(get_db)):
    try:
        return service_obtener_personas(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener personas: {str(e)}"
        )

# GET: /personas/{persona_id}
@router.get(
    "/{persona_id}", 
    response_model=PersonaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Obtener persona por ID",
    description="Retorna una persona específica por su UUID"
)
def obtener_persona(
    persona_id: UUID,  # CORREGIDO: int -> UUID
    db: Session = Depends(get_db)
):
    try:
        persona = service_obtener_persona_por_id(db, persona_id)
        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona con ID {persona_id} no encontrada"
            )
        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener persona: {str(e)}"
        )

# POST: /personas
@router.post(
    "/", 
    response_model=PersonaRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva persona",
    description="Crea una nueva persona con validaciones de documento y email únicos"
)
def crear_persona(
    persona: PersonaCrear, 
    db: Session = Depends(get_db)
):
    try:
        return service_crear_persona(db, persona)
    except Exception as e:
        # Capturar errores de duplicado (documento o email ya existen)
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear persona: {str(e)}"
        )

# PUT: /personas/{persona_id}
@router.put(
    "/{persona_id}",
    response_model=PersonaRespuesta,
    status_code=status.HTTP_200_OK,
    summary="Actualizar persona",
    description="Actualiza una persona existente"
)
def actualizar_persona(
    persona_id: UUID,
    persona_data: PersonaActualizar,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_actualizar_persona(db, persona_id, persona_data)
        if resultado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona con ID {persona_id} no encontrada"
            )
        return resultado
    except HTTPException:
        raise
    except Exception as e:
        if "ya existe" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar persona: {str(e)}"
        )

# DELETE: /personas/{persona_id}
@router.delete(
    "/{persona_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar persona",
    description="Elimina una persona (solo si no tiene registros relacionados)"
)
def eliminar_persona(
    persona_id: UUID,
    db: Session = Depends(get_db)
):
    try:
        resultado = service_eliminar_persona(db, persona_id)
        if not resultado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona con ID {persona_id} no encontrada"
            )
        return None  # 204 No Content
    except HTTPException:
        raise
    except Exception as e:
        if "registros relacionados" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar la persona porque tiene registros asociados"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar persona: {str(e)}"
        )