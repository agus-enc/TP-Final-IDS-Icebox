import uuid
import requests
from werkzeug.utils import secure_filename
from ..constants import SUPABASE_URL, SUPABASE_KEY, BUCKET_NAME

def subir_archivo_supabase(file_bytes: bytes, filename: str, content_type: str, subcarpeta: str, bucket_name: str = BUCKET_NAME) -> str:
    """
    Sube bytes puros a cualquier bucket de Supabase.
    """
    if len(file_bytes) == 0:
        raise ValueError({"errors": [{"code": "empty_file", "message": "El archivo llegó vacío (0 bytes)."}]})

    nombre_seguro = secure_filename(filename)
    codigo_unico = str(uuid.uuid4())[:8]
    ruta_en_bucket = f"{subcarpeta}/{codigo_unico}_{nombre_seguro}"

    url_upload = f"{SUPABASE_URL}/storage/v1/object/{bucket_name}/{ruta_en_bucket}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": content_type
    }

    respuesta = requests.post(url_upload, headers=headers, data=file_bytes)

    if not respuesta.ok:
        error_real = respuesta.text
        print(f"ERROR DE SUPABASE: {error_real}")
        raise ValueError({"errors": [{"code": "storage_error", "message": f"Fallo real en Supabase: {error_real}"}]})

    url_publica = f"{SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{ruta_en_bucket}"

    return url_publica

def subir_imagen_parada(archivo_flask, id_viaje: int) -> str:
    """
    Arma el "DTO" de una imagen para ser subida a Supabase
    """
    return subir_archivo_supabase(
        file_bytes=archivo_flask.read(),
        filename=archivo_flask.filename,
        content_type=archivo_flask.content_type,
        subcarpeta=f"viaje_{id_viaje}",
        bucket_name=BUCKET_NAME
    )

def borrar_imagen_supabase(url_publica: str) -> bool:
    """
    Toma cualquier URL pública de Supabase, auto-detecta el bucket
    y la ruta interna, y ejecuta el borrado.
    """
    if not url_publica:
        return False

    try:
        if "/object/public/" not in url_publica:
            return False

        parte_derecha = url_publica.split("/object/public/")[1]
        # [0] es el bucket dinámico, [1] es la ruta exacta del archivo
        bucket_detectado, ruta_en_bucket = parte_derecha.split("/", 1)

        url_delete = f"{SUPABASE_URL}/storage/v1/object/{bucket_detectado}/{ruta_en_bucket}"

        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }

        respuesta = requests.delete(url_delete, headers=headers)

        if not respuesta.ok:
            print(f"ERROR AL BORRAR EN SUPABASE: {respuesta.text}")
            return False

        return True

    except Exception as e:
        print(f"Error interno al intentar borrar imagen: {str(e)}")
        return False