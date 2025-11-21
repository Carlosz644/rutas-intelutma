from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/entregas", tags=["Entregas"])

# Listar entregas
@router.get("/", response_model=List[schemas.Entrega])
def listar_entregas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_entregas(db, skip=skip, limit=limit)

# Obtener entrega por ID
@router.get("/{id_entrega}", response_model=schemas.Entrega)
def obtener_entrega(id_entrega: int, db: Session = Depends(get_db)):
    entrega = crud.get_entrega(db, id_entrega)
    if not entrega:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return entrega

# Crear entrega
@router.post("/", response_model=schemas.Entrega)
def crear_entrega(entrega: schemas.EntregaBase, db: Session = Depends(get_db)):
    return crud.create_entrega(db, entrega)

# Actualizar entrega
@router.put("/{id_entrega}", response_model=schemas.Entrega)
def actualizar_entrega(id_entrega: int, entrega: schemas.EntregaBase, db: Session = Depends(get_db)):
    actualizada = crud.update_entrega(db, id_entrega, entrega)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return actualizada

# Eliminar entrega
@router.delete("/{id_entrega}", response_model=schemas.Entrega)
def eliminar_entrega(id_entrega: int, db: Session = Depends(get_db)):
    eliminada = crud.delete_entrega(db, id_entrega)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return eliminada
