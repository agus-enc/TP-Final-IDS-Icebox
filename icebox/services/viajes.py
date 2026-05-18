from .. import db
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

    nuevo_id = db.insertar_viaje(
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