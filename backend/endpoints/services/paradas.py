import json
from ..dao.usuarios import obtener_usuario_por_viaje
from ..dao.lugares import obtener_ciudad_por_id
from ..dao.paradas import insertar_parada_con_iman, eliminar_parada_por_id, eliminar_relato_parada_db, actualizar_relato_parada_db, actualizar_ciudad_parada_db, actualizar_parada_completa, obtener_paradas_por_viaje
from ..validators.paradas import validar_body_parada, validar_relato, validar_ciudad, validar_edicion_parada
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
    """Obtiene las paradas y mapea las llaves para compatibilidad con el frontend."""
    validar_minimo(id_viaje, 1, 'id_viaje')

    paradas_db = obtener_paradas_por_viaje(id_viaje)

    resultados_formateados = []
    for parada in paradas_db:
        resultados_formateados.append({
            "id_parada": parada["id_parada"],
            "id_viaje": parada["id_viaje"],
            "id_ciudad": parada["id_ciudad"],
            "nombre_ciudad": parada["nombre_ciudad"],
            "texto_resena": parada["relato_texto"],  # Renombra a lo que espera Jinja
            "orden_en_ruta": parada["orden_en_ruta"]
        })

    return resultados_formateados

def eliminar_parada(id_parada: int) -> bool:
    """Elimina un parada por id. Retorna True si existía y fue eliminado, False si no existía."""
    return eliminar_parada_por_id(id_parada)

def eliminar_relato(id_parada: int) -> bool:
    """Busca la parada y pone su columna relato_texto en NULL. Retorna True si se modificó, False si la parada no existía."""
    return eliminar_relato_parada_db(id_parada)

def modificar_relato_parada(id_parada: int, body: dict) -> dict:
    """Valida y actualiza únicamente el relato de la parada."""
    body_validado = validar_relato(body)
    relato_str = json.dumps(body_validado['relato_texto'])
    actualizar_relato_parada_db(id_parada, relato_str)
    
    return {"status": "success", "message": "Relato de la parada actualizado correctamente."}

def modificar_ciudad_parada(id_parada: int, body: dict) -> dict:
    """Valida y actualiza únicamente la ciudad de la parada."""
    body_validado = validar_ciudad(body)
    actualizar_ciudad_parada_db(id_parada, body_validado['id_ciudad'])
    
    return {"status": "success", "message": "Ciudad de la parada actualizada correctamente."}

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