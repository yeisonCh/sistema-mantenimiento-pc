# app/services/persona.py

from sqlalchemy.orm import Session
from repositories.persona import (
    obtener_personas,
    obtener_persona_por_id,
    obtener_persona_por_documento,
    obtener_persona_por_email,
    crear_persona,
    actualizar_persona,
    eliminar_persona
)
from schemas.persona import PersonaCrear, PersonaActualizar
from uuid import UUID
from typing import List

# Obtener todas las personas
def service_obtener_personas(db: Session):
    """Obtener todas las personas"""
    return obtener_personas(db)

# Obtener persona por ID
def service_obtener_persona_por_id(db: Session, persona_id: UUID):
    """Obtener una persona por su ID"""
    return obtener_persona_por_id(db, persona_id)

# Crear nueva persona (con validaciones de negocio)
def service_crear_persona(db: Session, persona: PersonaCrear):
    """
    Crear una nueva persona
    - Valida que el número de documento no exista
    - Valida que el email no exista (si se proporciona)
    """
    # Validación: ¿Ya existe una persona con ese número de documento?
    existe_documento = obtener_persona_por_documento(db, persona.numero_documento)
    if existe_documento:
        raise Exception(f"Ya existe una persona con el documento '{persona.numero_documento}'")
    
    # Validación: ¿Ya existe una persona con ese email?
    if persona.email:
        existe_email = obtener_persona_por_email(db, persona.email)
        if existe_email:
            raise Exception(f"Ya existe una persona con el email '{persona.email}'")
    
    return crear_persona(db, persona)

# Actualizar persona existente
def service_actualizar_persona(
    db: Session, 
    persona_id: UUID, 
    persona_data: PersonaActualizar
):
    """
    Actualizar una persona existente
    - Valida que la persona existe
    - Valida que el nuevo documento no pertenezca a otra persona
    - Valida que el nuevo email no pertenezca a otra persona
    """
    # Validación 1: ¿Existe la persona?
    existe = obtener_persona_por_id(db, persona_id)
    if not existe:
        raise Exception(f"Persona con ID {persona_id} no encontrada")
    
    # Validación 2: Si está actualizando el documento, ¿el nuevo documento ya existe en otra persona?
    if persona_data.numero_documento:
        doc_existe = obtener_persona_por_documento(db, persona_data.numero_documento)
        if doc_existe and doc_existe.id != persona_id:
            raise Exception(f"Ya existe otra persona con el documento '{persona_data.numero_documento}'")
    
    # Validación 3: Si está actualizando el email, ¿el nuevo email ya existe en otra persona?
    if persona_data.email:
        email_existe = obtener_persona_por_email(db, persona_data.email)
        if email_existe and email_existe.id != persona_id:
            raise Exception(f"Ya existe otra persona con el email '{persona_data.email}'")
    
    return actualizar_persona(db, persona_id, persona_data)

# Eliminar persona
def service_eliminar_persona(db: Session, persona_id: UUID):
    """
    Eliminar una persona
    - Valida que la persona existe
    """
    # Validación: ¿Existe la persona?
    existe = obtener_persona_por_id(db, persona_id)
    if not existe:
        raise Exception(f"Persona con ID {persona_id} no encontrada")
    
    return eliminar_persona(db, persona_id)