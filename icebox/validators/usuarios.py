from ..utils import construir_error, validar_entero, validar_minimo

def validar_id_usuario(id_usuario: int) -> int:
    return validar_minimo(id_usuario, 0, 'id')