from ..utils import validar_minimo

def validar_id_pais(id_pais: int) -> int:
    """Valida que el ID del cumpla con el valor minimo """
    return validar_minimo(id_pais, 1, 'id_pais')

def validar_codigo_pais(codigo):
    if not isinstance(codigo, str) or len(codigo) != 3:
        raise ValueError("El código de país debe ser un string de 3 letras (formato ISO).")
    return codigo.upper()
