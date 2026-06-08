from ..dao.viajes import insertar_viaje, eliminar_viaje_por_id, actualizar_titulo_viaje, obtener_viaje, obtener_viajes_por_usuario_db
from ..validators.viajes import validar_body_viaje, validar_id_viaje

def construir_viaje_dto(viaje: dict) -> dict:
    """ Construye el dict de respuesta básico de un viaje. """
    return {
        "id_viaje": viaje["id_viaje"],
        "id_usuario": viaje["id_usuario"],
        "titulo": viaje["titulo"],
        "fecha_viaje": viaje["fecha_viaje"]
    }

def obtener_viaje_por_id(id_viaje: int) -> dict:
    viaje = validar_id_viaje(id_viaje)
    return construir_viaje_dto(viaje)

def crear_viaje(body: dict, id_usuario: int) -> dict:
    """ Crea un nuevo viaje aplicando validaciones de DTO """
    datos_limpios = validar_body_viaje(body)

    nuevo_id = insertar_viaje(
        id_usuario=id_usuario,
        titulo=datos_limpios["titulo"],
        fecha_viaje=datos_limpios["fecha_viaje"]
    )

    return construir_viaje_dto({
        "id_viaje": nuevo_id,
        "id_usuario": id_usuario,
        "titulo": datos_limpios["titulo"],
        "fecha_viaje": datos_limpios["fecha_viaje"]
        })

def eliminar_viaje(id_viaje: int) -> bool:
    """Elimina un viaje por id. Retorna True si existía y fue eliminado, False si no existía."""
    return eliminar_viaje_por_id(id_viaje)

def obtener_todos_los_viajes() -> list:
    """Obtiene la lista completa de viajes desde la base de datos"""
    return "" # obtener_todos_los_viajes_db()

def editar_titulo_viaje(id_viaje: int, body: dict) -> bool:
    """Valida y actualiza el titulo de viaje existente"""
    datos_viaje = validar_body_viaje(body)
    titulo_limpio = datos_viaje.get("titulo")
    return actualizar_titulo_viaje(id_viaje, titulo_limpio)

def obtener_viajes_por_usuario(id_usuario: int) -> list:
    """Obtiene y formatea la lista de viajes de un usuario a formato dto"""
    lista = obtener_viajes_por_usuario_db(id_usuario)
    return [construir_viaje_dto(v) for v in lista]
