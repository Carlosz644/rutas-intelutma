from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import crud, schemas 

# Define el router
router = APIRouter(prefix="/rutas", tags=["Rutas"])

# --- ENDPOINTS CRUD BÁSICOS ---

# Endpoint GET para leer todas las rutas (Usa DB y CRUD)
@router.get("/", response_model=List[schemas.Ruta])
def listar_rutas_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Lista todas las rutas de entrega registradas en la base de datos.
    """
    rutas = crud.get_rutas(db, skip=skip, limit=limit)
    return rutas

# --- ENDPOINT DE OPTIMIZACIÓN CENTRAL ---

class ClienteIDs(schemas.BaseModel):
    """Esquema de entrada para el endpoint de optimización."""
    cliente_ids: List[int]
    # Opcional: Podrías añadir aquí el ID de la ruta o del conductor si fuera necesario

@router.post(
    "/optimizar", 
    response_model=List[schemas.ResultadoRutaOptimizada]
)
def optimizar_ruta_endpoint(
    cliente_ids_body: ClienteIDs, 
    db: Session = Depends(get_db)
):
    """
    Calcula el orden óptimo de visita para una lista de clientes (simulación TSP).
    """
    # Llama a la función de simulación de optimización en CRUD
    ruta_optimizada = crud.mock_optimize_route(db, cliente_ids_body.cliente_ids)
    
    # Nota: Aquí es donde en el futuro se llamará al algoritmo TSP real.
    return ruta_optimizada