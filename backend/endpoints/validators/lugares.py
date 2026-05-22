from ..utils import validar_minimo

def validar_id_pais(id_pais: int) -> int:
    """Valida que el ID del cumpla con el valor minimo """
    return validar_minimo(id_pais, 1, 'id_pais')
