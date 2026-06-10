def construir_error(code: str, message: str, description: str, level: str = 'error'):
    return {
        'errors': [{
            'code': code,
            'message': message,
            'level': level,
            'description': description
        }]
    }

def validar_entero(numero: str) -> int:
    try:
        return int(numero)
    except ValueError:
        raise ValueError(construir_error(
            code='invalid.int.format',
            message=f"Formato de '{numero}' inválido",
            description=f"El valor '{numero}' no puede convertirse a un número entero"
        ))

def validar_minimo(valor: int, minimo: int, nombre: str) -> int:
    if valor < minimo:
        raise ValueError(construir_error(
            code='invalid.min.value',
            message='Valor por debajo del mínimo permitido',
            description=f"El parámetro '{nombre}' debe ser mayor a {minimo}. Se recibió: {valor}"
        ))

    return valor