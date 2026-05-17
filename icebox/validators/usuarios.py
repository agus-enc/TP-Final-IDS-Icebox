from ..utils import construir_error, validar_entero, validar_minimo

def validar_id_usuario(id_usuario: str) -> int:
    id_usuario = validar_entero(id_usuario)
    return validar_minimo(id_usuario, 0, 'id')