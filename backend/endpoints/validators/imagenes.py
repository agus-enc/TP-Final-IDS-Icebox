from ..utils import construir_error

def validar_datos_imagen_viaje(id_viaje_str, tipo: str) -> dict:
    """Valida la forma de los datos de entrada para subir una imagen."""
    errores = []

    try:
        id_viaje = int(id_viaje_str)
        if id_viaje <= 0:
            errores.append(construir_error("invalid.id", "El ID del viaje debe ser positivo.", "Error"))
    except (ValueError, TypeError):
        errores.append(construir_error("invalid.id", "El ID del viaje debe ser numérico.", "Error"))

    tipo_limpio = str(tipo).strip().lower()
    if tipo_limpio not in ['header', 'diario']:
        errores.append(construir_error("invalid.tipo", "El tipo debe ser 'header' o 'diario'.", "Error"))

    if errores:
        raise ValueError({"errors": errores}, 400)

    return {
        "id_viaje": id_viaje,
        "tipo": tipo_limpio
    }