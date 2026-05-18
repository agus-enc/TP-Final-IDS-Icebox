import os
import uuid
from werkzeug.utils import secure_filename
from ..validators.imagenes import validar_imagen
from ..constants import UPLOAD_FOLDER, STATIC_URL_PATH

def subir_imagen(archivo) -> dict:
    """ Guarda físicamente la imagen en el servidor y retorna su DTO asegurandose que se cumplen las reglas de negocio """
    validar_imagen(archivo)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Genera nombre único seguro
    nombre_seguro = secure_filename(archivo.filename)
    nombre_unico = f"{uuid.uuid4().hex[:8]}_{nombre_seguro}"

    ruta_absoluta = os.path.join(UPLOAD_FOLDER, nombre_unico)
    archivo.save(ruta_absoluta)

    return {
        "url": f"{STATIC_URL_PATH}{nombre_unico}"
    }