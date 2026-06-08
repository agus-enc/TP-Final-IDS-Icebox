from ..dao.imagenes import contar_imagenes_viaje_por_tipo_db, insertar_imagen_viaje_db, actualizar_portada_viaje_db, obtener_imagenes_viaje_db, eliminar_portada_viaje_db, obtener_imagen_por_id_db, eliminar_imagen_por_id_db, actualizar_datos_imagen_db
from ..dao.viajes import obtener_viaje
from ..dao.usuarios import obtener_usuario_por_viaje
from ..services.storage import subir_imagen_parada
from .storage import borrar_imagen_supabase

def agregar_imagen_viaje(id_viaje: int, tipo: str, archivo_imagen, orden: int = 0, epigrafe: str = "") -> dict:
    """Orquesta las reglas de negocio (límites), la subida a Supabase y el guardado en BD."""

    id_usuario = obtener_usuario_por_viaje(id_viaje)

    # Regla de Negocio: Límites Máximos
    cantidad_actual = contar_imagenes_viaje_por_tipo_db(id_viaje, tipo)

    if tipo == 'header' and cantidad_actual >= 1:
        # Busca la URL de la portada vieja ANTES de sobrescribirla
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
    insertar_imagen_viaje_db(id_usuario, id_viaje, url_publica, tipo, orden, epigrafe)

    return {"mensaje": "Imagen subida", "url": url_publica, "tipo": tipo}

def obtener_imagenes_viaje(id_viaje: int) -> list:
    """
    Obtiene y formatea las imágenes de un viaje.
    Aplica validación de negocio y programación defensiva contra valores nulos de MySQL.
    """
    # Regla de Negocio: Validar que el viaje padre exista
    if not obtener_viaje(id_viaje):
        raise ValueError({"errors": [{"code": "not_found", "message": "El viaje solicitado no existe."}]}, 404)

    resultados_db = obtener_imagenes_viaje_db(id_viaje)
    imagenes_formateadas = []

    if not resultados_db:
        return []

    for img in resultados_db:
        if not isinstance(img, dict):
            continue

        imagenes_formateadas.append({
            "id_imagen": img.get("id_imagen"),
            "imagen_url": img.get("imagen_url") or "",
            "tipo": img.get("tipo") or "diario",
            "orden": img.get("orden") or 0,
            "epigrafe": img.get("epigrafe") or ""
        })

    return imagenes_formateadas

def eliminar_portada_viaje(id_viaje: int) -> bool:
    """Borra la portada de un viaje de la BD y de Supabase"""
    # Busca la URL de la portada ANTES de borrarla
    imagenes = obtener_imagenes_viaje_db(id_viaje)
    url_portada = next((img['imagen_url'] for img in imagenes if img['tipo'] == 'header'), None)

    eliminado_db = eliminar_portada_viaje_db(id_viaje)

    # Si se borró de MySQL y existía una URL, borrarla de Supabase
    if eliminado_db and url_portada:
        borrar_imagen_supabase(url_portada)

    return eliminado_db

def eliminar_imagen_diario(id_imagen: int) -> bool:
    """Borra la foto de la BD y, si existe, limpia Supabase"""
    imagen = obtener_imagen_por_id_db(id_imagen)
    if not imagen:
        return False

    eliminado = eliminar_imagen_por_id_db(id_imagen)
    if eliminado and imagen['imagen_url']:
        borrar_imagen_supabase(imagen['imagen_url'])

    return eliminado

def actualizar_datos_imagen(id_imagen: int, orden: int, epigrafe: str) -> bool:
    return actualizar_datos_imagen_db(id_imagen, orden, epigrafe)