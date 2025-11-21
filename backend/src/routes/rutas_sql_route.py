from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/rutas-sql", tags=["Rutas (SQL)"])

# Listar rutas
@router.get("/", response_model=List[schemas.Ruta])
def listar_rutas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_rutas(db, skip=skip, limit=limit)

# Obtener ruta por ID
@router.get("/{id_ruta}", response_model=schemas.Ruta)
def obtener_ruta(id_ruta: int, db: Session = Depends(get_db)):
    ruta = crud.get_ruta(db, id_ruta)
    if not ruta:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return ruta

# Crear ruta
@router.post("/", response_model=schemas.Ruta)
def crear_ruta(ruta: schemas.RutaBase, db: Session = Depends(get_db)):
    return crud.create_ruta(db, ruta)

# Actualizar ruta
@router.put("/{id_ruta}", response_model=schemas.Ruta)
def actualizar_ruta(id_ruta: int, ruta: schemas.RutaBase, db: Session = Depends(get_db)):
    actualizada = crud.update_ruta(db, id_ruta, ruta)
    if not actualizada:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return actualizada

# Eliminar ruta
@router.delete("/{id_ruta}", response_model=schemas.Ruta)
def eliminar_ruta(id_ruta: int, db: Session = Depends(get_db)):
    eliminada = crud.delete_ruta(db, id_ruta)
    if not eliminada:
        raise HTTPException(status_code=404, detail="Ruta no encontrada")
    return eliminada
