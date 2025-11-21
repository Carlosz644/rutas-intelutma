from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Listar clientes
@router.get("/", response_model=List[schemas.Cliente])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clientes(db, skip=skip, limit=limit)

# Obtener un cliente por ID
@router.get("/{id_cliente}", response_model=schemas.Cliente)
def obtener_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = crud.get_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Crear cliente
@router.post("/", response_model=schemas.Cliente)
def crear_cliente(cliente: schemas.ClienteBase, db: Session = Depends(get_db)):
    return crud.create_cliente(db, cliente)

# Actualizar cliente
@router.put("/{id_cliente}", response_model=schemas.Cliente)
def actualizar_cliente(id_cliente: int, cliente: schemas.ClienteBase, db: Session = Depends(get_db)):
    actualizado = crud.update_cliente(db, id_cliente, cliente)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return actualizado

# Eliminar cliente
@router.delete("/{id_cliente}", response_model=schemas.Cliente)
def eliminar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    eliminado = crud.delete_cliente(db, id_cliente)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return eliminado
