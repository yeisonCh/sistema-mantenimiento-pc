# app/repositories/persona.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.persona import Persona
from schemas.persona import PersonaCrear, PersonaActualizar
from uuid import UUID
from typing import List, Optional

# Obtener todas las personas
def obtener_personas(db: Session) -> List[Persona]:
    """Obtener todas las personas ordenadas por apellidos y nombres"""
    try:
        return db.query(Persona).order_by(Persona.apellidos, Persona.nombres).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error al obtener personas: {str(e)}")

# Obtener persona por ID
def obtener_persona_por_id(db: Session, persona_id: UUID) -> Optional[Persona]:
    """Obtener una persona por su UUID"""
    try:
        return db.query(Persona).filter(Persona.id == persona_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar persona: {str(e)}")

# Obtener persona por número de documento (para validar unicidad)
def obtener_persona_por_documento(db: Session, numero_documento: str) -> Optional[Persona]:
    """Obtener una persona por su número de documento"""
    try:
        return db.query(Persona).filter(Persona.numero_documento == numero_documento.strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por documento: {str(e)}")

# Obtener persona por email (para validar unicidad)
def obtener_persona_por_email(db: Session, email: str) -> Optional[Persona]:
    """Obtener una persona por su email"""
    try:
        return db.query(Persona).filter(Persona.email == email.lower().strip()).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error al buscar por email: {str(e)}")

# Crear nueva persona
def crear_persona(db: Session, persona: PersonaCrear) -> Persona:
    """Crear una nueva persona"""
    try:
        nueva_persona = Persona(
            nombres=persona.nombres.strip().title(),
            apellidos=persona.apellidos.strip().title(),
            tipo_documento=persona.tipo_documento.strip().upper(),
            numero_documento=persona.numero_documento.strip(),
            telefono=persona.telefono.strip() if persona.telefono else None,
            email=persona.email.lower().strip() if persona.email else None
        )
        
        db.add(nueva_persona)
        db.commit()
        db.refresh(nueva_persona)
        
        return nueva_persona
        
    except IntegrityError as e:
        db.rollback()
        # Detectar si es por documento duplicado o email duplicado
        if "duplicate" in str(e).lower() or "unique" in str(e).lower():
            raise Exception(f"Error: Ya existe una persona con ese documento o email")
        raise Exception(f"Error de integridad al crear persona: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al crear persona: {str(e)}")

# Actualizar persona existente
def actualizar_persona(
    db: Session, 
    persona_id: UUID, 
    persona_data: PersonaActualizar
) -> Optional[Persona]:
    """Actualizar una persona existente"""
    try:
        persona = obtener_persona_por_id(db, persona_id)
        
        if not persona:
            return None
        
        # Actualizar solo los campos que vienen en la petición
        if persona_data.nombres is not None:
            persona.nombres = persona_data.nombres.strip().title()
        
        if persona_data.apellidos is not None:
            persona.apellidos = persona_data.apellidos.strip().title()
        
        if persona_data.tipo_documento is not None:
            persona.tipo_documento = persona_data.tipo_documento.strip().upper()
        
        if persona_data.numero_documento is not None:
            persona.numero_documento = persona_data.numero_documento.strip()
        
        if persona_data.telefono is not None:
            persona.telefono = persona_data.telefono.strip() if persona_data.telefono else None
        
        if persona_data.email is not None:
            persona.email = persona_data.email.lower().strip() if persona_data.email else None
        
        db.commit()
        db.refresh(persona)
        
        return persona
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: Ya existe otra persona con ese documento o email")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al actualizar persona: {str(e)}")

# Eliminar persona
def eliminar_persona(db: Session, persona_id: UUID) -> bool:
    """Eliminar una persona"""
    try:
        persona = obtener_persona_por_id(db, persona_id)
        
        if not persona:
            return False
        
        db.delete(persona)
        db.commit()
        
        return True
        
    except IntegrityError as e:
        db.rollback()
        raise Exception(f"Error: No se puede eliminar la persona porque tiene registros relacionados")
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error al eliminar persona: {str(e)}")