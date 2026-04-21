from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.empresa import EmpresaCrear, EmpresaRespuesta
from services.empresa import service_obtener_empresas, service_obtener_empresa_por_id, service_crear_empresa

router = APIRouter(
    prefix="/empresas",
    tags=["Empresas"]
)

@router.get("/", response_model=list[EmpresaRespuesta])
def listar_empresas(db: Session = Depends(get_db)):
    return service_obtener_empresas(db)

@router.get("/{empresa_id}", response_model=EmpresaRespuesta)
def obtener_empresa(empresa_id: int, db: Session = Depends(get_db)):
    empresa = service_obtener_empresa_por_id(db, empresa_id)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@router.post("/", response_model=EmpresaRespuesta)
def crear_empresa(empresa: EmpresaCrear, db: Session = Depends(get_db)):
    return service_crear_empresa(db, empresa)