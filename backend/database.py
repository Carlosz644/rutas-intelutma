import os
# Eliminamos 'from dotenv import load_dotenv' porque no la usaremos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# =================================================================
# SOLUCIÓN TEMPORAL DE EMERGENCIA
# La URL está cableada directamente aquí para evitar el error del .env
# =================================================================
# Ponemos la URL directamente. Es vital que esta URL esté correcta:
DATABASE_URL = "mysql+pymysql://root:123456789@localhost:3306/ruta_de_entrega"

if not DATABASE_URL:
    # Esta línea ahora nunca debería ejecutarse
    raise ValueError("La variable de entorno DATABASE_URL no está configurada.")

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función de utilidad para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()