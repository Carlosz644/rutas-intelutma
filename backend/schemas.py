from pydantic import BaseModel, Field
from datetime import date, time, datetime
from typing import List, Optional
import enum

# Re-uso del Enum (Pydantic lo maneja bien)
class EstadoEntrega(str, enum.Enum):
    pendiente = "pendiente"
    en_camino = "en camino"
    entregado = "entregado"
    retrasado = "retrasado"

# ----------------------------------------------------
# --- 1. SCHEMAS BASE (Para crear o actualizar) ---
# ----------------------------------------------------

class ClienteBase(BaseModel):
    nombre: str = Field(..., description="Nombre completo o razón social del cliente.")
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    # Usamos float para manejar DECIMAL de la base de datos
    latitud: Optional[float] = None
    longitud: Optional[float] = None

class ConductorBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    licencia: Optional[str] = None

class VehiculoBase(BaseModel):
    marca: str
    modelo: str
    placas: str
    capacidad: int

class RutaBase(BaseModel):
    # Campos que se guardan en la tabla 'rutas'
    nombre_ruta: str
    id_conductor: int
    id_vehiculo: int
    fecha: date # Usamos date para el campo DATE de SQL

class EntregaBase(BaseModel):
    id_ruta: int
    id_cliente: int
    estado: Optional[EstadoEntrega] = EstadoEntrega.pendiente
    fecha_entrega: date
    hora_entrega: time
    observaciones: Optional[str] = None

class PaqueteBase(BaseModel):
    id_entrega: int
    descripcion: Optional[str] = None
    # Usamos float para manejar DECIMAL de la base de datos
    peso: Optional[float] = None
    valor: Optional[float] = None

class SeguimientoBase(BaseModel):
    id_entrega: int
    estado: EstadoEntrega
    comentario: Optional[str] = None

# ----------------------------------------------------
# --- 2. SCHEMAS COMPLETOS (Para respuesta de la API) ---
# ----------------------------------------------------

class Cliente(ClienteBase):
    id_cliente: int
    
    class Config:
        from_attributes = True

class Conductor(ConductorBase):
    id_conductor: int
    
    class Config:
        from_attributes = True

class Vehiculo(VehiculoBase):
    id_vehiculo: int
    
    class Config:
        from_attributes = True

class Ruta(RutaBase):
    # ESTE ES EL MODELO LIMPIO DE LA BASE DE DATOS
    id_ruta: int
    
    # AÑADIDO: Método extra para manejar la serialización de tipos
    # Esto es CRUCIAL para evitar el error 500 al devolver objetos de SQLAlchemy
    # que contienen tipos como decimal.Decimal o datetime.date.
    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
        }

class Entrega(EntregaBase):
    id_entrega: int
    
    class Config:
        from_attributes = True

class Paquete(PaqueteBase):
    id_paquete: int
    
    class Config:
        from_attributes = True

class Seguimiento(SeguimientoBase):
    id_seguimiento: int
    fecha: datetime 
    
    class Config:
        from_attributes = True

# ----------------------------------------------------
# --- 3. SCHEMAS PARA RESULTADOS CALCULADOS (Optimización) ---
# ----------------------------------------------------

class ResultadoRutaOptimizada(BaseModel):
    """Modelo usado para el resultado de un punto en una ruta optimizada, incluye métricas de distancia/tiempo."""
    nombre: str
    direccion: str
    # Usamos float para la serialización de coordenadas
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    distancia_km: Optional[float] = None
    duracion_min: Optional[float] = None
    
    class Config:
        from_attributes = True

class ListaClientesOptimizar(BaseModel):
    cliente_ids: List[int] = Field(..., description="Lista de IDs de clientes a visitar.")