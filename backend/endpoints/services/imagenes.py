import os
import uuid
from werkzeug.utils import secure_filename
from ..constants import UPLOAD_FOLDER, STATIC_URL_PATH
from ..dao.imagenes import contar_imagenes_viaje_por_tipo_db, insertar_imagen_viaje_db, actualizar_portada_viaje_db, obtener_imagenes_viaje_db, eliminar_portada_viaje_db
from ..dao.viajes import obtener_viaje
from ..dao.usuarios import obtener_usuario_por_viaje
from ..services.storage import subir_imagen_parada
from .storage import borrar_imagen_supabase
from rembg import remove
from PIL import Image
from ..utils import construir_error

def agregar_imagen_viaje(id_viaje: int, tipo: str, archivo_imagen) -> dict:
    """Orquesta las reglas de negocio (límites), la subida a Supabase y el guardado en BD."""

    # 1. Regla de Negocio: Existencia
    if not obtener_viaje(id_viaje):
        raise ValueError({"errors": [{"code": "not_found", "message": "El viaje no existe."}]}, 404)

    id_usuario = obtener_usuario_por_viaje(id_viaje)

    # 2. Regla de Negocio: Límites Máximos
    cantidad_actual = contar_imagenes_viaje_por_tipo_db(id_viaje, tipo)

    if tipo == 'header' and cantidad_actual >= 1:
        # Buscar la URL de la portada vieja ANTES de sobrescribirla
        imagenes_existentes = obtener_imagenes_viaje_db(id_viaje)
        url_portada_vieja = next((img['imagen_url'] for img in imagenes_existentes if img['tipo'] == 'header'), None)

        url_publica_nueva = subir_imagen_parada(archivo_imagen, id_viaje)
        actualizar_portada_viaje_db(id_viaje, url_publica_nueva)

        if url_portada_vieja:
            borrar_imagen_supabase(url_portada_vieja)

        return {"mensaje": "Portada actualizada", "url": url_publica_nueva, "tipo": tipo}

    if tipo == 'diario' and cantidad_actual >= 10:
        raise ValueError({"errors": [{"code": "limit_reached", "message": "Límite de 10 imágenes alcanzado."}]}, 403)

    url_publica = subir_imagen_parada(archivo_imagen, id_viaje)
    insertar_imagen_viaje_db(id_usuario, id_viaje, url_publica, tipo)

    return {"mensaje": "Imagen subida", "url": url_publica, "tipo": tipo}

def eliminar_portada_viaje(id_viaje: int) -> bool:
    # 1. Buscar la URL de la portada ANTES de borrarla
    imagenes = obtener_imagenes_viaje_db(id_viaje)
    url_portada = next((img['imagen_url'] for img in imagenes if img['tipo'] == 'header'), None)

    eliminado_db = eliminar_portada_viaje_db(id_viaje)

    # 2. Si se borró de MySQL y existía una URL, borrarla de Supabase
    if eliminado_db and url_portada:
        borrar_imagen_supabase(url_portada)

    return eliminado_db

def remover_fondo(archivo) -> dict:
    """ Le saca el fondo a la imagen, la guarda como .png en el disco y devuelve su DTO  """
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