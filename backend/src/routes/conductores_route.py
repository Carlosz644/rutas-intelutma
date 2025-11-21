from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/conductores", tags=["Conductores"])

# Listar conductores
@router.get("/", response_model=List[schemas.Conductor])
def listar_conductores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_conductores(db, skip=skip, limit=limit)

# Obtener conductor por ID
@router.get("/{id_conductor}", response_model=schemas.Conductor)
def obtener_conductor(id_conductor: int, db: Session = Depends(get_db)):
    conductor = crud.get_conductor(db, id_conductor)
    if not conductor:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return conductor

# Crear conductor
@router.post("/", response_model=schemas.Conductor)
def crear_conductor(conductor: schemas.ConductorBase, db: Session = Depends(get_db)):
    return crud.create_conductor(db, conductor)

# Actualizar conductor
@router.put("/{id_conductor}", response_model=schemas.Conductor)
def actualizar_conductor(id_conductor: int, conductor: schemas.ConductorBase, db: Session = Depends(get_db)):
    actualizado = crud.update_conductor(db, id_conductor, conductor)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return actualizado

# Eliminar conductor
@router.delete("/{id_conductor}", response_model=schemas.Conductor)
def eliminar_conductor(id_conductor: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_conductor(db, id_conductor)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Conductor no encontrado")
    return eliminado
