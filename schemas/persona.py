# app/schemas/persona.py

from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from uuid import UUID
import re

class PersonaCrear(BaseModel):
    nombres: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Nombres de la persona",
        example="Yeison Andrés"
    )
    apellidos: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Apellidos de la persona",
        example="Rodríguez Pérez"
    )
    tipo_documento: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="Tipo de documento (CC, CE, TI, PAS, NIT)",
        example="CC"
    )
    numero_documento: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description="Número de documento",
        example="12345678"
    )
    telefono: Optional[str] = Field(
        None,
        max_length=20,
        description="Teléfono de contacto",
        example="3001234567"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Correo electrónico",
        example="yeison@ejemplo.com"
    )
    
    @field_validator('nombres')
    @classmethod
    def validar_nombres(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Los nombres no pueden estar vacíos')
        
        v = v.strip().title()  # Normalizar: primera letra mayúscula
        
        # Solo letras, espacios, y caracteres especiales comunes
        if not re.match(r'^[A-Za-záéíóúñÑ\s]+$', v):
            raise ValueError('Los nombres solo pueden contener letras y espacios')
        
        if '  ' in v:
            raise ValueError('Los nombres no pueden tener espacios dobles')
        
        return v
    
    @field_validator('apellidos')
    @classmethod
    def validar_apellidos(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Los apellidos no pueden estar vacíos')
        
        v = v.strip().title()
        
        if not re.match(r'^[A-Za-záéíóúñÑ\s]+$', v):
            raise ValueError('Los apellidos solo pueden contener letras y espacios')
        
        if '  ' in v:
            raise ValueError('Los apellidos no pueden tener espacios dobles')
        
        return v
    
    @field_validator('tipo_documento')
    @classmethod
    def validar_tipo_documento(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El tipo de documento no puede estar vacío')
        
        v = v.strip().upper()
        
        # Tipos de documento comunes en Colombia
        tipos_validos = ['CC', 'CE', 'TI', 'PAS', 'NIT', 'RUT']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de documento inválido. Válidos: {", ".join(tipos_validos)}')
        
        return v
    
    @field_validator('numero_documento')
    @classmethod
    def validar_numero_documento(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('El número de documento no puede estar vacío')
        
        v = v.strip()
        
        # Solo números y opcionalmente guión (para NIT)
        if not re.match(r'^\d+(-\d{1,2})?$', v):
            raise ValueError('El número de documento solo puede contener números (opcionalmente guión para NIT)')
        
        return v
    
    @field_validator('telefono')
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        v = v.strip()
        
        # Validar formato teléfono (opcional +57 luego números)
        if not re.match(r'^(\+?57)?[\d\s\-\(\)]{7,15}$', v):
            raise ValueError('Formato de teléfono inválido')
        
        return v


class PersonaActualizar(BaseModel):
    """Para actualizar persona (todos los campos opcionales)"""
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    tipo_documento: Optional[str] = Field(None, min_length=2, max_length=20)
    numero_documento: Optional[str] = Field(None, min_length=5, max_length=20)
    telefono: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    
    @field_validator('nombres')
    @classmethod
    def validar_nombres(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Los nombres no pueden estar vacíos')
        return v.strip().title()
    
    @field_validator('apellidos')
    @classmethod
    def validar_apellidos(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Los apellidos no pueden estar vacíos')
        return v.strip().title()
    
    @field_validator('tipo_documento')
    @classmethod
    def validar_tipo_documento(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El tipo de documento no puede estar vacío')
        
        v = v.strip().upper()
        tipos_validos = ['CC', 'CE', 'TI', 'PAS', 'NIT', 'RUT']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de documento inválido. Válidos: {", ".join(tipos_validos)}')
        
        return v
    
    @field_validator('numero_documento')
    @classmethod
    def validar_numero_documento(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('El número de documento no puede estar vacío')
        
        if not re.match(r'^\d+(-\d{1,2})?$', v.strip()):
            raise ValueError('El número de documento solo puede contener números')
        
        return v.strip()


class PersonaRespuesta(BaseModel):
    """Respuesta de persona (lo que se devuelve al cliente)"""
    id: UUID
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    telefono: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True