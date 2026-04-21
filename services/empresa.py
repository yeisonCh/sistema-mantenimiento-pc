from sqlalchemy.orm import Session
from repositories.empresa import obtener_empresas, obtener_empresa_por_id, crear_empresa
from schemas.empresa import EmpresaCrear

def service_obtener_empresas(db: Session):
    return obtener_empresas(db)

def service_obtener_empresa_por_id(db: Session, empresa_id: int):
    return obtener_empresa_por_id(db, empresa_id)

def service_crear_empresa(db: Session, empresa: EmpresaCrear):
    return crear_empresa(db, empresa)