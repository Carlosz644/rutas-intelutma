from pydantic import BaseModel, Field, EmailStr
from datetime import date, time, datetime
from typing import List, Optional
import enum

# ============================================
# ENUMS COMPARTIDOS
# ============================================

class EstadoEntrega(str, enum.Enum):
    pendiente = "pendiente"
    en_camino = "en camino"
    entregado = "entregado"
    retrasado = "retrasado"


# ============================================
# 1. SCHEMAS BASE (CREACIÓN/ACTUALIZACIÓN)
# ============================================

class ClienteBase(BaseModel):
    nombre: str = Field(..., description="Nombre completo o razón social del cliente.")
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
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
    nombre_ruta: str
    id_conductor: int
    id_vehiculo: int
    fecha: date


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
    peso: Optional[float] = None
    valor: Optional[float] = None


class SeguimientoBase(BaseModel):
    id_entrega: int
    estado: EstadoEntrega
    comentario: Optional[str] = None


# ============================================
# 2. SCHEMAS COMPLETOS (RESPUESTA API)
# ============================================

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
    id_ruta: int

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


# ============================================
# 3. SCHEMAS PARA OPTIMIZACIÓN
# ============================================

class ResultadoRutaOptimizada(BaseModel):
    nombre: str
    direccion: str
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    distancia_km: Optional[float] = None
    duracion_min: Optional[float] = None

    class Config:
        from_attributes = True


class ListaClientesOptimizar(BaseModel):
    cliente_ids: List[int] = Field(..., description="Lista de IDs de clientes a visitar.")


# ============================================
# 4. SCHEMAS DE USUARIOS (ROLES Y AUTENTICACIÓN)
# ============================================

class RolUsuario(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    repartidor = "repartidor"


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: RolUsuario = RolUsuario.repartidor
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    rol: RolUsuario
    activo: bool
    creado_en: datetime

    class Config:
        from_attributes = True

class CambiarPassword(BaseModel):
    password_actual: str
    password_nueva: str
    confirmar_nueva: str

class EvidenciaBase(BaseModel):
    id_entrega: int
    url_foto: str
    tipo: str = "entrega"

class Evidencia(EvidenciaBase):
    id_evidencia: int
    fecha_subida: datetime

    class Config:
        orm_mode = True

