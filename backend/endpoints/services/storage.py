import uuid
import requests
from werkzeug.utils import secure_filename
from ..constants import SUPABASE_URL, SUPABASE_KEY, BUCKET_NAME

def subir_imagen_parada(archivo_flask, id_viaje: int) -> str:
    """
    Sube una imagen usando peticiones HTTP puras, esquivando los bugs de supabase-py.
    """

    # Leer bytes y validar
    bytes_archivo = archivo_flask.read()
    if len(bytes_archivo) == 0:
        raise ValueError({"errors": [{"code": "empty_file", "message": "El archivo llegó vacío (0 bytes)."}]})

    # Preparar nombres y rutas
    nombre_seguro = secure_filename(archivo_flask.filename)
    codigo_unico = str(uuid.uuid4())[:8]
    ruta_en_bucket = f"viaje_{id_viaje}/{codigo_unico}_{nombre_seguro}"
    tipo_contenido = archivo_flask.content_type

    # BYPASS HTTP (Conexión directa a la API de Supabase)
    url_upload = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{ruta_en_bucket}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": tipo_contenido
    }

    # Hace el POST binario
    respuesta = requests.post(url_upload, headers=headers, data=bytes_archivo)

    if not respuesta.ok:
        error_real = respuesta.text
        print(f"ERROR DE SUPABASE: {error_real}")
        raise ValueError({"errors": [{"code": "storage_error", "message": f"Fallo real en Supabase: {error_real}"}]})

    url_publica = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{ruta_en_bucket}"

    return url_publica

def borrar_imagen_supabase(url_publica: str) -> bool:
    """
    Toma la URL pública de Supabase, extrae la ruta interna y ejecuta un HTTP DELETE.
    """
    if not url_publica:
        return False

    try:
        # 1. Extrae la ruta exacta del archivo cortando la URL pública
        separador = f"/object/public/{BUCKET_NAME}/"
        if separador not in url_publica:
            return False
        ruta_en_bucket = url_publica.split(separador)[1]

        # 2. Arma la petición de borrado a la API
        url_delete = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{ruta_en_bucket}"

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