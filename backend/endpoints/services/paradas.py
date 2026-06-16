from ..dao.usuarios import obtener_usuario_por_viaje
from ..dao.lugares import obtener_ciudad_por_id
from ..dao.paradas import insertar_parada_con_iman, eliminar_parada_por_id, actualizar_parada_completa, obtener_paradas_por_viaje
from ..validators.paradas import validar_body_parada, validar_edicion_parada
from ..validators.viajes import validar_id_viaje
from ..dao.imanes import obtener_iman_por_parada, eliminar_iman_por_id
from .storage import borrar_imagen_supabase

def crear_parada(id_viaje: int, body: dict) -> dict:
    """ Verifica que el viaje de la parada exista, la crea y devuelve su DTO aplicando la logica de negocio. """
    viaje = validar_id_viaje(id_viaje)
    id_viaje = viaje["id_viaje"]

    datos_limpios = validar_body_parada(body)

    id_usuario = obtener_usuario_por_viaje(id_viaje)
    if not id_usuario:
        raise ValueError({"errors": [{"code": "not_found", "message": "El usuario no existe."}]}, 404)

    if not obtener_ciudad_por_id(datos_limpios['id_ciudad']):
        raise ValueError({"errors": [{"code": "not_found", "message": "La ciudad no existe."}]}, 404)

    imagen_url = datos_limpios.get('imagen_url')
    predeterminado = True if not imagen_url or not imagen_url.strip() else False

    relato_str = datos_limpios.get('texto_resena')

    ids_generados = insertar_parada_con_iman(
        id_viaje=id_viaje,
        id_usuario=id_usuario,
        id_ciudad=datos_limpios['id_ciudad'],
        orden_en_ruta=datos_limpios['orden_en_ruta'],
        relato_str=relato_str,
        imagen_url=imagen_url if not predeterminado else None,
        predeterminado=predeterminado
    )

    return {
        "id_parada": ids_generados["id_parada"],
        "id_iman": ids_generados["id_iman"],
        "id_viaje": id_viaje,
        "id_ciudad": datos_limpios['id_ciudad'],
        "orden_en_ruta": datos_limpios['orden_en_ruta'],
        "relato_texto": datos_limpios.get('relato_texto'),
        "iman": {
            "imagen_url": imagen_url,
            "predeterminado": predeterminado
        }
    }

def obtener_paradas_de_viaje(id_viaje: int) -> list:
    """
    Valida el id y obtiene las paradas enriquecidas directamente desde el DAO.
    """
    viaje = validar_id_viaje(id_viaje)
    id_viaje = viaje["id_viaje"]

    paradas_db = obtener_paradas_por_viaje(id_viaje)

    return paradas_db

def eliminar_parada(id_parada: int) -> bool:
    """Elimina una parada por id, limpiando previamente su imán de Supabase y BD si corresponde."""
    iman = obtener_iman_por_parada(id_parada)
    if iman:
        if not iman.get('predeterminado') and iman.get('imagen_url'):
            borrar_imagen_supabase(iman['imagen_url'])
        eliminar_iman_por_id(iman['id_iman'])

    return eliminar_parada_por_id(id_parada)

def editar_parada_completa(id_parada: int, body: dict) -> bool:
    """Valida y actualiza ciudad y texto de una parada existente."""
    datos_limpios = validar_edicion_parada(body)

    if not obtener_ciudad_por_id(datos_limpios['id_ciudad']):
        raise ValueError({"errors": [{"code": "not_found", "message": "La ciudad no existe."}]}, 404)

    return actualizar_parada_completa(
        id_parada=id_parada,
        id_ciudad=datos_limpios['id_ciudad'],
        texto_resena=datos_limpios.get('texto_resena', '')
    )