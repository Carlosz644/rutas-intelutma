from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# --- 1. Importaciones de Rutas (Tus rutas de negocio) ---
from backend.src.routes.rutas_route import router as rutas_router
from backend.src.routes.geocode_route import router as geocode_router
from backend.src.routes.directions_route import router as directions_router
from backend.src.routes.matrix_route import router as matrix_router
from backend.src.routes.optimize_route import router as optimize_router
from backend.src.routes.users_route import router as users_router

# --- 2. Importaciones de Base de Datos y Modelos (LÓGICA SQL/DB VERIFICADA) ---
# Importa la Sesión y el Engine desde .database
from .database import SessionLocal, engine
# Importa los modelos ORM 
from . import models 

# --- 3. Inicialización de la Base de Datos (LÓGICA SQL/DB VERIFICADA) ---
# Crea las tablas definidas en models.py si aún no existen en MySQL (ejecutar UNA vez)
models.Base.metadata.create_all(bind=engine)

# --- 4. Inicialización de la Aplicación FastAPI (UNA SOLA VEZ) ---
app = FastAPI(title="API de Rutas de Entrega Optimizada")

# --- 5. Dependencia para Obtener la Sesión de Base de Datos (LÓGICA SQL/DB VERIFICADA) ---
def get_db():
    """Generador que proporciona una sesión de base de datos y asegura su cierre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 6. Registro de Rutas (Tus routers de negocio) ---
app.include_router(rutas_router)
app.include_router(geocode_router)
app.include_router(directions_router)
app.include_router(matrix_router)
app.include_router(optimize_router)
app.include_router(users_router)