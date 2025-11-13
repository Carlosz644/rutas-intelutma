from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import enum

from backend import models, schemas
from backend.models import Cliente, Conductor, Vehiculo, Ruta, Entrega, Paquete, Seguimiento

# --- Algoritmo de Optimización Simulado (TSP) ---
BASE_LAT = 20.9168
BASE_LON = -101.3508

def get_rutas_optimizar(db: Session, cliente_ids: List[int]) -> List[schemas.ResultadoRutaOptimizada]:
    """
    Simula la optimización de una ruta.
    
    Por simplicidad, esta función solo recupera los clientes
    y los ordena por latitud (del más al menos al norte) para simular una ruta lógica.
    """
    
    # 1. Obtener la información de los clientes seleccionados
    clientes = db.query(Cliente).filter(Cliente.id_cliente.in_(cliente_ids)).all()
    
    # 2. Ordenar a los clientes (Simulación TSP: ordenar por latitud)
    # Ordenar por latitud de forma descendente (los más al norte primero)
    clientes_ordenados = sorted(
        clientes,
        key=lambda c: c.latitud if c.latitud is not None else -float('inf'), # Asegura el manejo de None
        reverse=True
    )
    
    # 3. Preparar la lista de resultados, incluyendo la Base de Operaciones
    resultados: List[schemas.ResultadoRutaOptimizada] = []
    
    # Primera parada: BASE DE OPERACIONES
    resultados.append(schemas.ResultadoRutaOptimizada(
        nombre="BASE DE OPERACIONES",
        direccion="Calle Ficticia #100, Centro",
        latitud=BASE_LAT,
        longitud=BASE_LON,
        distancia_km=0.0,
        duracion_min=0.0
    ))
    
    # Simulación de acumulación (distancia y duración)
    distancia_acumulada = 0.0
    duracion_acumulada = 0.0
    
    # 4. Procesar las paradas de los clientes
    for cliente in clientes_ordenados:
        # Lógica de Simulación de Distancia/Duración
        # Aquí se simula un cálculo simple, en un proyecto real se usaría una API de Mapas
        distancia_segmento = abs(cliente.latitud - BASE_LAT) * 100.0 + abs(cliente.longitud - BASE_LON) * 50.0
        duracion_segmento = distancia_segmento * 2.5 # Simula 2.5 minutos por km
        
        distancia_acumulada += distancia_segmento
        duracion_acumulada += duracion_segmento
        
        resultados.append(schemas.ResultadoRutaOptimizada(
            nombre=cliente.nombre,
            direccion=cliente.direccion,
            latitud=float(cliente.latitud) if cliente.latitud is not None else None,
            longitud=float(cliente.longitud) if cliente.longitud is not None else None,
            distancia_km=round(distancia_acumulada, 2),
            duracion_min=round(duracion_acumulada, 2)
        ))
        
    return resultados


# --- Funciones CRUD Estándar ---

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene clientes con paginación."""
    return db.query(Cliente).offset(skip).limit(limit).all()

def get_rutas(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene rutas con paginación."""
    # Usamos .all() para cargar las rutas
    return db.query(Ruta).offset(skip).limit(limit).all()

def get_conductores(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene conductores con paginación."""
    return db.query(Conductor).offset(skip).limit(limit).all()

# Añade otras funciones CRUD (get_vehiculos, get_entregas, etc.) si son necesarias.