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

# ===============================
# CRUD COMPLETO DE CLIENTES
# ===============================

def get_cliente(db: Session, id_cliente: int):
    """Obtiene un cliente por su ID."""
    return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()


def create_cliente(db: Session, cliente: schemas.ClienteBase):
    """Crea un nuevo cliente en la base de datos."""
    nuevo = Cliente(
        nombre=cliente.nombre,
        direccion=cliente.direccion,
        telefono=cliente.telefono,
        correo=cliente.correo,
        latitud=cliente.latitud,
        longitud=cliente.longitud,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_cliente(db: Session, id_cliente: int, cliente_data: schemas.ClienteBase):
    """Actualiza un cliente existente."""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        return None

    cliente.nombre = cliente_data.nombre
    cliente.direccion = cliente_data.direccion
    cliente.telefono = cliente_data.telefono
    cliente.correo = cliente_data.correo
    cliente.latitud = cliente_data.latitud
    cliente.longitud = cliente_data.longitud

    db.commit()
    db.refresh(cliente)
    return cliente


def delete_cliente(db: Session, id_cliente: int):
    """Elimina un cliente por ID."""
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    if not cliente:
        return None

    db.delete(cliente)
    db.commit()
    return cliente


# ===============================
# CRUD COMPLETO DE CONDUCTORES
# ===============================

def get_conductor(db: Session, id_conductor: int):
    """Obtiene un conductor por ID."""
    return db.query(Conductor).filter(Conductor.id_conductor == id_conductor).first()


def create_conductor(db: Session, conductor: schemas.ConductorBase):
    """Crea un nuevo conductor."""
    nuevo = Conductor(
        nombre=conductor.nombre,
        telefono=conductor.telefono,
        licencia=conductor.licencia,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_conductor(db: Session, id_conductor: int, conductor_data: schemas.ConductorBase):
    """Actualiza un conductor existente."""
    db_conductor = db.query(Conductor).filter(Conductor.id_conductor == id_conductor).first()
    if not db_conductor:
        return None

    db_conductor.nombre = conductor_data.nombre
    db_conductor.telefono = conductor_data.telefono
    db_conductor.licencia = conductor_data.licencia

    db.commit()
    db.refresh(db_conductor)
    return db_conductor


def delete_conductor(db: Session, id_conductor: int):
    """Elimina un conductor."""
    db_conductor = db.query(Conductor).filter(Conductor.id_conductor == id_conductor).first()
    if not db_conductor:
        return None

    db.delete(db_conductor)
    db.commit()
    return db_conductor

# ===============================
# CRUD COMPLETO DE VEHÍCULOS
# ===============================

def get_vehiculo(db: Session, id_vehiculo: int):
    """Obtiene un vehículo por ID."""
    return db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()


def get_vehiculos(db: Session, skip: int = 0, limit: int = 100):
    """Lista vehículos con paginación."""
    return db.query(Vehiculo).offset(skip).limit(limit).all()


def create_vehiculo(db: Session, vehiculo: schemas.VehiculoBase):
    """Crea un vehículo nuevo en la base de datos."""
    nuevo = Vehiculo(
        marca=vehiculo.marca,
        modelo=vehiculo.modelo,
        placas=vehiculo.placas,
        capacidad=vehiculo.capacidad,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_vehiculo(db: Session, id_vehiculo: int, vehiculo_data: schemas.VehiculoBase):
    """Actualiza un vehículo existente."""
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None

    vehiculo.marca = vehiculo_data.marca
    vehiculo.modelo = vehiculo_data.modelo
    vehiculo.placas = vehiculo_data.placas
    vehiculo.capacidad = vehiculo_data.capacidad

    db.commit()
    db.refresh(vehiculo)
    return vehiculo


def delete_vehiculo(db: Session, id_vehiculo: int):
    """Elimina un vehículo."""
    vehiculo = db.query(Vehiculo).filter(Vehiculo.id_vehiculo == id_vehiculo).first()
    if not vehiculo:
        return None

    db.delete(vehiculo)
    db.commit()
    return vehiculo

# ===============================
# CRUD COMPLETO DE RUTAS
# ===============================

def get_ruta(db: Session, id_ruta: int):
    """Obtiene una ruta por ID."""
    return db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()


def get_rutas(db: Session, skip: int = 0, limit: int = 100):
    """Lista rutas con paginación."""
    return db.query(Ruta).offset(skip).limit(limit).all()


def create_ruta(db: Session, ruta: schemas.RutaBase):
    """Crea una nueva ruta."""
    nueva = Ruta(
        nombre_ruta=ruta.nombre_ruta,
        id_conductor=ruta.id_conductor,
        id_vehiculo=ruta.id_vehiculo,
        fecha=ruta.fecha,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_ruta(db: Session, id_ruta: int, ruta_data: schemas.RutaBase):
    """Actualiza una ruta existente."""
    ruta = db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()
    if not ruta:
        return None

    ruta.nombre_ruta = ruta_data.nombre_ruta
    ruta.id_conductor = ruta_data.id_conductor
    ruta.id_vehiculo = ruta_data.id_vehiculo
    ruta.fecha = ruta_data.fecha

    db.commit()
    db.refresh(ruta)
    return ruta


def delete_ruta(db: Session, id_ruta: int):
    """Elimina una ruta por ID."""
    ruta = db.query(Ruta).filter(Ruta.id_ruta == id_ruta).first()
    if not ruta:
        return None

    db.delete(ruta)
    db.commit()
    return 

# ===============================
# CRUD COMPLETO DE ENTREGAS
# ===============================

def get_entrega(db: Session, id_entrega: int):
    """Obtiene una entrega por su ID."""
    return db.query(Entrega).filter(Entrega.id_entrega == id_entrega).first()


def get_entregas(db: Session, skip: int = 0, limit: int = 100):
    """Lista entregas con paginación."""
    return db.query(Entrega).offset(skip).limit(limit).all()


def create_entrega(db: Session, entrega: schemas.EntregaBase):
    """Crea una nueva entrega."""
    nueva = Entrega(
        id_ruta=entrega.id_ruta,
        id_cliente=entrega.id_cliente,
        estado=entrega.estado,
        fecha_entrega=entrega.fecha_entrega,
        hora_entrega=entrega.hora_entrega,
        observaciones=entrega.observaciones,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def update_entrega(db: Session, id_entrega: int, entrega_data: schemas.EntregaBase):
    """Actualiza una entrega existente."""
    entrega = db.query(Entrega).filter(Entrega.id_entrega == id_entrega).first()
    if not entrega:
        return None

    entrega.id_ruta = entrega_data.id_ruta
    entrega.id_cliente = entrega_data.id_cliente
    entrega.estado = entrega_data.estado
    entrega.fecha_entrega = entrega_data.fecha_entrega
    entrega.hora_entrega = entrega_data.hora_entrega
    entrega.observaciones = entrega_data.observaciones

    db.commit()
    db.refresh(entrega)
    return entrega


def delete_entrega(db: Session, id_entrega: int):
    """Elimina una entrega."""
    entrega = db.query(Entrega).filter(Entrega.id_entrega == id_entrega).first()
    if not entrega:
        return None

    db.delete(entrega)
    db.commit()
    return entrega

# ===============================
# CRUD COMPLETO DE PAQUETES
# ===============================

def get_paquete(db: Session, id_paquete: int):
    """Obtiene un paquete por su ID."""
    return db.query(Paquete).filter(Paquete.id_paquete == id_paquete).first()


def get_paquetes(db: Session, skip: int = 0, limit: int = 100):
    """Lista paquetes con paginación."""
    return db.query(Paquete).offset(skip).limit(limit).all()


def create_paquete(db: Session, paquete: schemas.PaqueteBase):
    """Crea un paquete nuevo."""
    nuevo = Paquete(
        id_entrega=paquete.id_entrega,
        descripcion=paquete.descripcion,
        peso=paquete.peso,
        valor=paquete.valor,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_paquete(db: Session, id_paquete: int, paquete_data: schemas.PaqueteBase):
    """Actualiza un paquete existente."""
    paquete = db.query(Paquete).filter(Paquete.id_paquete == id_paquete).first()
    if not paquete:
        return None

    paquete.id_entrega = paquete_data.id_entrega
    paquete.descripcion = paquete_data.descripcion
    paquete.peso = paquete_data.peso
    paquete.valor = paquete_data.valor

    db.commit()
    db.refresh(paquete)
    return paquete


def delete_paquete(db: Session, id_paquete: int):
    """Elimina un paquete."""
    paquete = db.query(Paquete).filter(Paquete.id_paquete == id_paquete).first()
    if not paquete:
        return None

    db.delete(paquete)
    db.commit()
    return paquete

# ===============================
# CRUD COMPLETO DE SEGUIMIENTO
# ===============================

def get_seguimiento(db: Session, id_seguimiento: int):
    """Obtiene un seguimiento por ID."""
    return db.query(Seguimiento).filter(Seguimiento.id_seguimiento == id_seguimiento).first()


def get_seguimientos(db: Session, skip: int = 0, limit: int = 100):
    """Lista todos los seguimientos."""
    return db.query(Seguimiento).offset(skip).limit(limit).all()


def get_seguimientos_por_entrega(db: Session, id_entrega: int):
    """Obtiene todos los seguimientos asociados a una entrega."""
    return db.query(Seguimiento).filter(Seguimiento.id_entrega == id_entrega).order_by(Seguimiento.fecha.asc()).all()


def create_seguimiento(db: Session, seguimiento: schemas.SeguimientoBase):
    """Crea un registro de seguimiento."""
    nuevo = Seguimiento(
        id_entrega=seguimiento.id_entrega,
        estado=seguimiento.estado,
        comentario=seguimiento.comentario,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_seguimiento(db: Session, id_seguimiento: int, seguimiento_data: schemas.SeguimientoBase):
    """Actualiza un registro de seguimiento."""
    seg = db.query(Seguimiento).filter(Seguimiento.id_seguimiento == id_seguimiento).first()
    if not seg:
        return None

    seg.id_entrega = seguimiento_data.id_entrega
    seg.estado = seguimiento_data.estado
    seg.comentario = seguimiento_data.comentario

    db.commit()
    db.refresh(seg)
    return seg


def delete_seguimiento(db: Session, id_seguimiento: int):
    """Elimina un seguimiento."""
    seg = db.query(Seguimiento).filter(Seguimiento.id_seguimiento == id_seguimiento).first()
    if not seg:
        return None

    db.delete(seg)
    db.commit()
    return seg

# ============================================
# 🧩 CRUD PARA USUARIOS
# ============================================

from backend.models import Usuario, RolUsuario

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()


def get_usuario_por_id(db: Session, id_usuario: int):
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def get_usuario_por_correo(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def create_usuario(db: Session, usuario: schemas.UsuarioCreate, password_hash: str):
    nuevo = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password_hash=password_hash,  
        rol=usuario.rol,
        activo=1 if usuario.activo else 0,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def update_usuario(db: Session, id_usuario: int, usuario_data: schemas.UsuarioBase):
    usuario = get_usuario_por_id(db, id_usuario)
    if not usuario:
        return None

    usuario.nombre = usuario_data.nombre
    usuario.correo = usuario_data.correo
    usuario.rol = usuario_data.rol
    usuario.activo = 1 if usuario_data.activo else 0

    db.commit()
    db.refresh(usuario)
    return usuario


def delete_usuario(db: Session, id_usuario: int):
    usuario = get_usuario_por_id(db, id_usuario)
    if not usuario:
        return None

    db.delete(usuario)
    db.commit()
    return usuario


def cambiar_password(db: Session, id_usuario: int, password_hash: str):
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    if not usuario:
        return None

    usuario.password_hash = password_hash
    db.commit()
    db.refresh(usuario)
    return usuario

from backend.models import Evidencia

def create_evidencia(db: Session, evidencia: schemas.EvidenciaBase):
    nueva = Evidencia(
        id_entrega=evidencia.id_entrega,
        url_foto=evidencia.url_foto,
        tipo=evidencia.tipo
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


def get_evidencias_por_entrega(db: Session, id_entrega: int):
    return db.query(Evidencia).filter(Evidencia.id_entrega == id_entrega).all()

