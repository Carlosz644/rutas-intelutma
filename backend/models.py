from __future__ import annotations
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Date, Time, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from backend.database import Base 


# ============================================
# ENUMS
# ============================================

class EstadoEntrega(str, enum.Enum):
    pendiente = "pendiente"
    en_camino = "en camino"
    entregado = "entregado"
    retrasado = "retrasado"


class RolUsuario(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    repartidor = "repartidor"


# ============================================
# 1. CLIENTES
# ============================================

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    correo = Column(String(100))
    latitud = Column(DECIMAL(10, 7))
    longitud = Column(DECIMAL(10, 7))

    entregas = relationship("Entrega", back_populates="cliente")


# ============================================
# 2. CONDUCTORES
# ============================================

class Conductor(Base):
    __tablename__ = "conductores"

    id_conductor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    licencia = Column(String(50))

    rutas = relationship("Ruta", back_populates="conductor")


# ============================================
# 3. VEHÍCULOS
# ============================================

class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    placas = Column(String(20))
    capacidad = Column(Integer)

    rutas = relationship("Ruta", back_populates="vehiculo")


# ============================================
# 4. RUTAS
# ============================================

class Ruta(Base):
    __tablename__ = "rutas"

    id_ruta = Column(Integer, primary_key=True, index=True)
    nombre_ruta = Column(String(100))
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"))
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))
    fecha = Column(Date)

    conductor = relationship("Conductor", back_populates="rutas")
    vehiculo = relationship("Vehiculo", back_populates="rutas")
    entregas = relationship("Entrega", back_populates="ruta")


# ============================================
# 5. ENTREGAS
# ============================================

class Entrega(Base):
    __tablename__ = "entregas"

    id_entrega = Column(Integer, primary_key=True, index=True)
    id_ruta = Column(Integer, ForeignKey("rutas.id_ruta"))
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    estado = Column(Enum(EstadoEntrega), default=EstadoEntrega.pendiente)
    fecha_entrega = Column(Date)
    hora_entrega = Column(Time)
    observaciones = Column(Text)

    ruta = relationship("Ruta", back_populates="entregas")
    cliente = relationship("Cliente", back_populates="entregas")
    paquetes = relationship("Paquete", back_populates="entrega")
    seguimientos = relationship("Seguimiento", back_populates="entrega")


# ============================================
# 6. PAQUETES
# ============================================

class Paquete(Base):
    __tablename__ = "paquetes"

    id_paquete = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"))
    descripcion = Column(String(200))
    peso = Column(DECIMAL(10, 2))
    valor = Column(DECIMAL(10, 2))

    entrega = relationship("Entrega", back_populates="paquetes")


# ============================================
# 7. SEGUIMIENTO
# ============================================

class Seguimiento(Base):
    __tablename__ = "seguimiento"

    id_seguimiento = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"))
    fecha = Column(DateTime, default=func.now())
    estado = Column(Enum(EstadoEntrega))
    comentario = Column(Text)

    entrega = relationship("Entrega", back_populates="seguimientos")


# ============================================
# 8. USUARIOS
# ============================================

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolUsuario), default=RolUsuario.repartidor, nullable=False)
    activo = Column(Integer, default=1, nullable=False)
    creado_en = Column(DateTime, default=func.now())

class EvidenciaEntrega(Base):
    __tablename__ = "evidencias_entrega"

    id_evidencia = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"))
    url_foto = Column(String(500))
    tipo = Column(Enum("entrega", "documento", "cliente", "otro", name="tipo_evidencia"))
    fecha_subida = Column(DateTime, default=datetime.utcnow)

    entrega = relationship("Entrega")

