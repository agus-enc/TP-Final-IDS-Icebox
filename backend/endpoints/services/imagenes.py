import os
import uuid
from werkzeug.utils import secure_filename
from ..validators.imagenes import validar_imagen
from ..constants import UPLOAD_FOLDER, STATIC_URL_PATH
from rembg import remove
from PIL import Image
from ..utils import construir_error

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

def remover_fondo(archivo) -> dict:
    """ Le saca el fondo a la imagen, la guarda como .png en el disco y devuelve su DTO  """
    validar_imagen(archivo)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    imagen_original = Image.open(archivo.stream)

    try:
        imagen_sin_fondo = remove(imagen_original)  # Devuelve una nueva imagen sin fondo

        nombre_seguro = secure_filename(archivo.filename).rsplit('.', 1)[0]  # Borra la extension vieja
        nombre_unico = f"iman_{uuid.uuid4().hex[:8]}_{nombre_seguro}.png"

        ruta_absoluta = os.path.join(UPLOAD_FOLDER, nombre_unico)
        imagen_sin_fondo.save(ruta_absoluta, format="PNG")

        return {
            "url": f"{STATIC_URL_PATH}{nombre_unico}"
        }

    except OSError:
        # Error del disco duro (ej: carpeta uploads no existe, permisos denegados)
        raise ValueError({"errors": [
            construir_error("io_error", "Error de almacenamiento.", "No se pudo guardar la imagen en el servidor.")]},
                         500)

    except Exception as e:
        # Error de la librería de IA (rembg) u otros crasheos de procesamiento
        raise ValueError({"errors": [
            construir_error("processing_error", "Error al procesar la imagen.", "Falló la remoción de fondo.")]}, 500)