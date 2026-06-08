from ..utils import construir_error
from .viajes import validar_id_viaje

def validar_datos_imagen_viaje(id_viaje_str, tipo: str) -> dict:
    """Valida la forma de los datos de entrada para subir una imagen."""
    errores = []

    viaje_existente = validar_id_viaje(id_viaje_str)

    tipo_limpio = str(tipo).strip().lower()
    if tipo_limpio not in ['header', 'diario']:
        errores.append(construir_error("invalid.tipo", "El tipo debe ser 'header' o 'diario'.", "Error"))

    if errores:
        raise ValueError({"errors": errores}, 400)

    return {
        "id_viaje": viaje_existente["id_viaje"],
        "tipo": tipo_limpio
    }