def validar_codigo_pais(codigo):
    if not isinstance(codigo, str) or len(codigo) != 3:
        raise ValueError("El código de país debe ser un string de 3 letras (formato ISO).")
    return codigo.upper()
