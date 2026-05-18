from ..constants import (
    MIN_ID
)
from ..utils import validar_formato_fecha, construir_error, validar_entero, validar_minimo

def validar_body_viaje(body: dict) -> dict:
    """
    Valida que el JSON recibido contenga el título y una fecha válida.
    Retorna un diccionario limpio solo con los datos que interesan.
    """
    if not body:
        raise ValueError(construir_error(
            "invalid.body",
            "El cuerpo de la petición está vacío",
            "Se requiere un JSON con 'titulo' y 'fecha_viaje'"
        ))

    errores = []

    titulo = body.get("titulo")
    if not titulo or not isinstance(titulo, str) or not titulo.strip():
        errores.append(construir_error(
            code='invalid.titulo',
            message=f'Campo requerido: Titulo.',
            description=f"El titulo es un campo obligatorio."
        )['errors'][0])

    fecha_viaje = body.get("fecha_viaje")
    if not fecha_viaje or not isinstance(fecha_viaje, str):
        errores.append(construir_error(
            code='invalid.date',
            message=f'Campo requerido: Fecha.',
            description=f"La fecha es un campo obligatorio."
        )['errors'][0])
    else:
        try:
            validar_formato_fecha(fecha_viaje)
        except ValueError as e:
            errores.extend(e.args[0]['errors'])

    if errores:
        raise ValueError({"errors": errores})

    return {
        "titulo": titulo.strip(),
        "fecha_viaje": fecha_viaje
    }

def validar_id_viaje(id_str: str) -> int:
    """Valida que el id del viaje recibido en la URL sea un entero válido y mayor a cero."""
    id_viaje = validar_entero(id_str, 'id_viaje')
    return validar_minimo(id_viaje, MIN_ID, 'id_viaje')

def validar_id_parada(id_str: str) -> int:
    """Valida que el id de la parada recibido en la URL sea un entero válido y mayor a cero."""
    id_parada = validar_entero(id_str, 'id_parada')
    return validar_minimo(id_parada, MIN_ID, 'id_parada')