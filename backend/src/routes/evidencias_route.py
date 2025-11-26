from fastapi import APIRouter, File, UploadFile, Depends
import shutil
import uuid
from sqlalchemy.orm import Session

from backend.database import get_db
from backend import crud, schemas

router = APIRouter(prefix="/evidencias", tags=["Evidencias"])


@router.post("/subir/{id_entrega}")
def subir_evidencia(
    id_entrega: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Crear nombre único
    nombre_archivo = f"{uuid.uuid4()}.{file.filename.split('.')[-1]}"

    # Ruta donde se guardará físicamente
    ruta_guardado = f"backend/uploads/evidencias/{nombre_archivo}"

    # Guardar el archivo en el servidor
    with open(ruta_guardado, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # URL pública para acceder
    url_publica = f"/uploads/evidencias/{nombre_archivo}"

    # Guardar referencia en la base de datos
    evidencia = crud.create_evidencia(
        db,
        schemas.EvidenciaBase(
            id_entrega=id_entrega,
            url_foto=url_publica
        )
    )

    return evidencia
