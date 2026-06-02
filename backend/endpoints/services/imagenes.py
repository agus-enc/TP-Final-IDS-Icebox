from ..dao.imagenes import contar_imagenes_viaje_por_tipo_db, insertar_imagen_viaje_db, actualizar_portada_viaje_db, obtener_imagenes_viaje_db, eliminar_portada_viaje_db
from ..dao.viajes import obtener_viaje
from ..dao.usuarios import obtener_usuario_por_viaje
from ..services.storage import subir_imagen_parada
from .storage import borrar_imagen_supabase

def agregar_imagen_viaje(id_viaje: int, tipo: str, archivo_imagen) -> dict:
    """Orquesta las reglas de negocio (límites), la subida a Supabase y el guardado en BD."""

    # Regla de Negocio: Existencia
    if not obtener_viaje(id_viaje):
        raise ValueError({"errors": [{"code": "not_found", "message": "El viaje no existe."}]}, 404)

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
    insertar_imagen_viaje_db(id_usuario, id_viaje, url_publica, tipo)

    return {"mensaje": "Imagen subida", "url": url_publica, "tipo": tipo}

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