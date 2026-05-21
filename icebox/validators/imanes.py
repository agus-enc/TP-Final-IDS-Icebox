from ..constants import (
    MIN_ID
)

def validar_id_iman(id_str: str) -> int:
    """Valida que el id del imán recibido en la URL sea un entero válido y mayor a cero."""
    id_iman = validar_entero(id_str, 'id_iman')
    return validar_minimo(id_iman, MIN_ID, 'id_iman')