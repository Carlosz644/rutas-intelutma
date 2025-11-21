from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import crud
from backend.auth import verify_password, create_access_token

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = crud.get_usuario_por_correo(db, form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Correo o contraseña incorrectos")

    token = create_access_token({
        "id_usuario": user.id_usuario,
        "rol": user.rol
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": user.rol
    }
