from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import crud, schemas
from backend.auth import require_roles

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ======================================================
# Obtener todos los usuarios (solo super_admin y admin)
# ======================================================
@router.get("/", response_model=List[schemas.Usuario])
def listar_usuarios(
    db: Session = Depends(get_db),
    user=Depends(require_roles(["super_admin", "admin"]))
):
    return crud.get_usuarios(db)


# ======================================================
# Obtener usuario por ID (solo admin/super_admin)
# ======================================================
@router.get("/{id_usuario}", response_model=schemas.Usuario)
def obtener_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["super_admin", "admin"]))
):
    usuario = crud.get_usuario_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# ======================================================
# Crear nuevo usuario (solo super_admin)
# ======================================================
@router.post("/", response_model=schemas.Usuario)
def crear_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["super_admin"]))   # 🔐 Protegido
):

    existente = crud.get_usuario_por_correo(db, usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    from backend.auth import hash_password
    password_hash = hash_password(usuario.password)

    nuevo_usuario = crud.create_usuario(db, usuario, password_hash)
    return nuevo_usuario


# ======================================================
# Actualizar usuario (solo super_admin)
# ======================================================
@router.put("/{id_usuario}", response_model=schemas.Usuario)
def actualizar_usuario(
    id_usuario: int,
    usuario: schemas.UsuarioBase,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["super_admin"]))   # 🔐 Protegido
):
    actualizado = crud.update_usuario(db, id_usuario, usuario)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return actualizado


# ======================================================
# Eliminar usuario (solo super_admin)
# ======================================================
@router.delete("/{id_usuario}", response_model=schemas.Usuario)
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles(["super_admin"]))   # 🔐 Protegido
):
    eliminado = crud.delete_usuario(db, id_usuario)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return eliminado

from backend.auth import verify_password, hash_password, require_roles

@router.put(
    "/{id_usuario}/cambiar_password",
    dependencies=[Depends(require_roles(["super_admin"]))],
    tags=["Usuarios"]
)
def cambiar_password_admin(
    id_usuario: int,
    data: schemas.CambiarPassword,
    db: Session = Depends(get_db)
):
    usuario = crud.get_usuario_por_id(db, id_usuario)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Validación: confirmar contraseña nueva
    if data.password_nueva != data.confirmar_nueva:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    # Generar nuevo hash
    nuevo_hash = hash_password(data.password_nueva)

    actualizado = crud.cambiar_password(db, id_usuario, nuevo_hash)
    return {"mensaje": "Contraseña actualizada correctamente", "usuario": actualizado}

from backend.auth import get_current_user

@router.put(
    "/cambiar_mi_password",
    tags=["Usuarios"]
)
def cambiar_mi_password(
    data: schemas.CambiarPassword,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    # Validar contraseña actual
    if not verify_password(data.password_actual, current_user.password_hash):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")

    # Validación confirmación
    if data.password_nueva != data.confirmar_nueva:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")

    # Hash nuevo
    nuevo_hash = hash_password(data.password_nueva)

    actualizado = crud.cambiar_password(db, current_user.id_usuario, nuevo_hash)

    return {"mensaje": "Tu contraseña ha sido actualizada correctamente"}


