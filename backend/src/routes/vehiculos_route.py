from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

# Listar vehículos
@router.get("/", response_model=List[schemas.Vehiculo])
def listar_vehiculos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vehiculos(db, skip=skip, limit=limit)

# Obtener vehículo por ID
@router.get("/{id_vehiculo}", response_model=schemas.Vehiculo)
def obtener_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    vehiculo = crud.get_vehiculo(db, id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

# Crear vehículo
@router.post("/", response_model=schemas.Vehiculo)
def crear_vehiculo(vehiculo: schemas.VehiculoBase, db: Session = Depends(get_db)):
    return crud.create_vehiculo(db, vehiculo)

# Actualizar vehículo
@router.put("/{id_vehiculo}", response_model=schemas.Vehiculo)
def actualizar_vehiculo(id_vehiculo: int, vehiculo: schemas.VehiculoBase, db: Session = Depends(get_db)):
    actualizado = crud.update_vehiculo(db, id_vehiculo, vehiculo)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return actualizado

# Eliminar vehículo
@router.delete("/{id_vehiculo}", response_model=schemas.Vehiculo)
def eliminar_vehiculo(id_vehiculo: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_vehiculo(db, id_vehiculo)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return eliminado
