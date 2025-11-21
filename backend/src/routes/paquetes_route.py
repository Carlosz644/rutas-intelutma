from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/paquetes", tags=["Paquetes"])

# Listar paquetes
@router.get("/", response_model=List[schemas.Paquete])
def listar_paquetes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_paquetes(db, skip=skip, limit=limit)

# Obtener paquete por ID
@router.get("/{id_paquete}", response_model=schemas.Paquete)
def obtener_paquete(id_paquete: int, db: Session = Depends(get_db)):
    paquete = crud.get_paquete(db, id_paquete)
    if not paquete:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return paquete

# Crear paquete
@router.post("/", response_model=schemas.Paquete)
def crear_paquete(paquete: schemas.PaqueteBase, db: Session = Depends(get_db)):
    return crud.create_paquete(db, paquete)

# Actualizar paquete
@router.put("/{id_paquete}", response_model=schemas.Paquete)
def actualizar_paquete(id_paquete: int, paquete: schemas.PaqueteBase, db: Session = Depends(get_db)):
    actualizado = crud.update_paquete(db, id_paquete, paquete)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return actualizado

# Eliminar paquete
@router.delete("/{id_paquete}", response_model=schemas.Paquete)
def eliminar_paquete(id_paquete: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_paquete(db, id_paquete)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Paquete no encontrado")
    return eliminado
