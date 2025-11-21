from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import crud

# ===========================================================
# CONFIGURACIÓN JWT
# ===========================================================
SECRET_KEY = "SUPERSECRETO123"  # luego lo pasamos al .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ===========================================================
# UTILIDADES PARA CONTRASEÑAS
# ===========================================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# ===========================================================
# CREACIÓN Y VALIDACIÓN DE TOKENS
# ===========================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id_usuario")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

    user = crud.get_usuario_por_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user

# ===========================================================
# VALIDACIÓN DE ROLES
# ===========================================================

def require_roles(roles: list[str]):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.rol not in roles:
            raise HTTPException(status_code=403, detail="No tienes permisos suficientes")
        return current_user

    return role_checker
