from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/seguimiento", tags=["Seguimiento"])

# Listar seguimientos
@router.get("/", response_model=List[schemas.Seguimiento])
def listar_seguimientos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_seguimientos(db, skip=skip, limit=limit)

# Obtener seguimiento por ID
@router.get("/{id_seguimiento}", response_model=schemas.Seguimiento)
def obtener_seguimiento(id_seguimiento: int, db: Session = Depends(get_db)):
    seguimiento = crud.get_seguimiento(db, id_seguimiento)
    if not seguimiento:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return seguimiento

# Obtener seguimientos de una entrega
@router.get("/entrega/{id_entrega}", response_model=List[schemas.Seguimiento])
def seguimientos_por_entrega(id_entrega: int, db: Session = Depends(get_db)):
    return crud.get_seguimientos_por_entrega(db, id_entrega)

# Crear seguimiento
@router.post("/", response_model=schemas.Seguimiento)
def crear_seguimiento(seguimiento: schemas.SeguimientoBase, db: Session = Depends(get_db)):
    return crud.create_seguimiento(db, seguimiento)

# Actualizar seguimiento
@router.put("/{id_seguimiento}", response_model=schemas.Seguimiento)
def actualizar_seguimiento(id_seguimiento: int, seguimiento: schemas.SeguimientoBase, db: Session = Depends(get_db)):
    actualizado = crud.update_seguimiento(db, id_seguimiento, seguimiento)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return actualizado

# Eliminar seguimiento
@router.delete("/{id_seguimiento}", response_model=schemas.Seguimiento)
def eliminar_seguimiento(id_seguimiento: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_seguimiento(db, id_seguimiento)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Seguimiento no encontrado")
    return eliminado
