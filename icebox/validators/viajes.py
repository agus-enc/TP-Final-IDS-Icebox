from ..utils import validar_formato_fecha, construir_error

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
            description=f"El titulo es un campo obligatioro."
        )['errors'][0])

    fecha_viaje = body.get("fecha_viaje")
    if not fecha_viaje:
        errores.append(construir_error(
            code='invalid.date',
            message=f'Campo requerido: Fecha.',
            description=f"La fecha es un campo obligatorio."
        )['errors'][0])
    else:
        try:
            validar_formato_fecha(fecha_viaje, "%Y-%m-%d", "fecha_viaje")
        except ValueError:
            errores.append(construir_error(
                code='invalid.date',
                message=f'Campo requerido: Fecha.',
                description=f"La fecha {fecha_viaje} es invalida."
            )['errors'][0])

    if errores:
        raise ValueError({"errors": errores})

    return {
        "titulo": titulo.strip(),
        "fecha_viaje": fecha_viaje
    }