import json
from ..db import obtener_usuario_por_viaje, insertar_parada_con_iman, obtener_ciudad_por_id
from ..validators.paradas import validar_body_parada
from ..utils import validar_minimo

def crear_parada(id_viaje: int, body: dict) -> dict:
    """ Verifica que el viaje de la parada exista, la crea y devuelve su DTO aplicando la logica de negocio. """
    validar_minimo(id_viaje, 1, 'id_viaje')

    datos_limpios = validar_body_parada(body)

    id_usuario = obtener_usuario_por_viaje(id_viaje)
    if not id_usuario:
        raise ValueError({"errors": [{"code": "not_found", "message": "El viaje no existe."}]}, 404)

    if not obtener_ciudad_por_id(datos_limpios['id_ciudad']):
        raise ValueError({"errors": [{"code": "not_found", "message": "La ciudad no existe."}]}, 404)

    imagen_url = datos_limpios.get('imagen_url')
    predeterminado = True if not imagen_url or not imagen_url.strip() else False

    relato_str = json.dumps(datos_limpios['relato_texto']) if datos_limpios.get('relato_texto') else None

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

def eliminar_parada(id_parada: int) -> bool:
    """Elimina un parada por id. Retorna True si existía y fue eliminado, False si no existía."""
    return db.eliminar_parada_por_id(id_parada)