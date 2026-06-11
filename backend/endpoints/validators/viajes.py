from ..constants import (MIN_ID)
from ..utils import construir_error, validar_entero, validar_minimo
from ..dao.viajes import obtener_viaje

def validar_body_viaje(body: dict) -> dict:
    """
    Valida que el JSON recibido sea valido.
    Retorna un diccionario limpio solo con los datos que interesan.
    """
    if not body:
        raise ValueError(construir_error(
            "invalid.body",
            "El cuerpo de la petición está vacío",
            "Se requiere un JSON con 'titulo'"
        ))

    errores = []

    titulo = body.get("titulo")
    if not titulo or not isinstance(titulo, str) or not titulo.strip():
        errores.append(construir_error(
            code='invalid.titulo',
            message=f'Campo requerido: Titulo.',
            description=f"El titulo es un campo obligatorio."
        )['errors'][0])

    if errores:
        raise ValueError({"errors": errores})

    return {
        "titulo": titulo.strip(),
    }

def validar_id_viaje(id_str: str) -> dict:
    """Valida formato del ID y verifica que el viaje exista en la BD."""

    try:
        id_viaje = validar_entero(id_str)
        id_viaje = validar_minimo(id_viaje, MIN_ID, 'id_viaje')
    except ValueError as e:
        raise e

    viaje = obtener_viaje(id_viaje)
    if not viaje:
        error = construir_error(
            code="not_found",
            message="El viaje especificado no existe.",
            description="No se encontró un viaje con ese ID en la base de datos."
        )

        raise ValueError({"errors": [error]}, 404)

    return viaje