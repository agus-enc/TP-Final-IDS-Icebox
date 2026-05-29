from ..dao.viajes import insertar_viaje, eliminar_viaje_por_id
from ..validators.viajes import validar_body_viaje

def construir_viaje_dto(viaje: dict) -> dict:
    """ Construye el dict de respuesta básico de un viaje. """
    return {
        "id_viaje": viaje["id_viaje"],
        "id_usuario": viaje["id_usuario"],
        "titulo": viaje["titulo"],
        "fecha_viaje": viaje["fecha_viaje"]
    }

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
    return obtener_todos_los_viajes_db()
