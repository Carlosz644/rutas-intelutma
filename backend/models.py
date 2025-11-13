from __future__ import annotations # NECESARIO para referencias de tipos en SQLAlchemy (ej. relationship)
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, Date, Time, Text, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

# IMPORTACIÓN CRUCIAL: Asegura que la clase Base sea visible para main.py
from backend.database import Base 

# Definición del Enum para el estado de entrega (igual que en schemas.py)
class EstadoEntrega(str, enum.Enum):
    pendiente = "pendiente"
    en_camino = "en camino"
    entregado = "entregado"
    retrasado = "retrasado"

# ----------------------------------------------------
# 1. Tabla: CLIENTES
# ----------------------------------------------------
class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200))
    telefono = Column(String(20))
    correo = Column(String(100))
    latitud = Column(DECIMAL(10, 7))
    longitud = Column(DECIMAL(10, 7))
    
    # Relación con Entregas
    entregas = relationship("Entrega", back_populates="cliente")

# ----------------------------------------------------
# 2. Tabla: CONDUCTORES
# ----------------------------------------------------
class Conductor(Base):
    __tablename__ = "conductores"
    
    id_conductor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    licencia = Column(String(50))
    
    # Relación con Rutas
    rutas = relationship("Ruta", back_populates="conductor")

# ----------------------------------------------------
# 3. Tabla: VEHÍCULOS
# ----------------------------------------------------
class Vehiculo(Base):
    __tablename__ = "vehiculos"
    
    id_vehiculo = Column(Integer, primary_key=True, index=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    placas = Column(String(20))
    capacidad = Column(Integer)
    
    # Relación con Rutas
    rutas = relationship("Ruta", back_populates="vehiculo")

# ----------------------------------------------------
# 4. Tabla: RUTAS
# ----------------------------------------------------
class Ruta(Base):
    __tablename__ = "rutas"
    
    id_ruta = Column(Integer, primary_key=True, index=True)
    nombre_ruta = Column(String(100))
    id_conductor = Column(Integer, ForeignKey("conductores.id_conductor"))
    id_vehiculo = Column(Integer, ForeignKey("vehiculos.id_vehiculo"))
    fecha = Column(Date)
    
    # Relaciones
    conductor = relationship("Conductor", back_populates="rutas")
    vehiculo = relationship("Vehiculo", back_populates="rutas")
    entregas = relationship("Entrega", back_populates="ruta")

# ----------------------------------------------------
# 5. Tabla: ENTREGAS
# ----------------------------------------------------
class Entrega(Base):
    __tablename__ = "entregas"
    
    id_entrega = Column(Integer, primary_key=True, index=True)
    id_ruta = Column(Integer, ForeignKey("rutas.id_ruta"))
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"))
    # Usamos el Enum para mapear al ENUM de SQL
    estado = Column(Enum(EstadoEntrega), default=EstadoEntrega.pendiente)
    fecha_entrega = Column(Date)
    hora_entrega = Column(Time)
    observaciones = Column(Text)
    
    # Relaciones
    ruta = relationship("Ruta", back_populates="entregas")
    cliente = relationship("Cliente", back_populates="entregas")
    paquetes = relationship("Paquete", back_populates="entrega")
    seguimientos = relationship("Seguimiento", back_populates="entrega")

# ----------------------------------------------------
# 6. Tabla: PAQUETES
# ----------------------------------------------------
class Paquete(Base):
    __tablename__ = "paquetes"
    
    id_paquete = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"))
    descripcion = Column(String(200))
    peso = Column(DECIMAL(10, 2))
    valor = Column(DECIMAL(10, 2))

    # Relaciones
    entrega = relationship("Entrega", back_populates="paquetes")

# ----------------------------------------------------
# 7. Tabla: SEGUIMIENTO
# ----------------------------------------------------
class Seguimiento(Base):
    __tablename__ = "seguimiento"
    
    id_seguimiento = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"))
    fecha = Column(DateTime, default=func.now())
    estado = Column(Enum(EstadoEntrega))
    comentario = Column(Text)
    
    # Relaciones
    entrega = relationship("Entrega", back_populates="seguimientos")
