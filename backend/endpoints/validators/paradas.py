from ..constants import (MIN_ID)
from ..utils import construir_error, validar_entero, validar_minimo

def validar_body_parada(body: dict) -> dict:
    """ Valida los campos de una parada"""
    errores = []

    if not isinstance(body, dict):
        raise ValueError(
            {"errors": [construir_error(
                "invalid.body",
                "El body debe ser un objeto JSON.",
                "Formato incorrecto")]},400)

    id_ciudad = body.get('id_ciudad')
    if type(id_ciudad) is not int or id_ciudad <= 0:
        errores.append(construir_error(
            'invalid.id_ciudad',
            'El id_ciudad debe ser entero positivo.',
            'Requerido'))

    orden_en_ruta = body.get('orden_en_ruta')
    if type(orden_en_ruta) is not int or orden_en_ruta < 0:
        errores.append(construir_error(
            'invalid.orden',
            'El orden_en_ruta debe ser número positivo.',
            'Requerido'))

    imagen_url = body.get('imagen_url')
    if imagen_url is not None and not isinstance(imagen_url, str):
        errores.append(construir_error('invalid.imagen_url', 'La url debe ser texto.', 'Error'))

    texto_resena = body.get('texto_resena')
    if texto_resena is not None and not isinstance(texto_resena, str):
        errores.append(construir_error('invalid.texto', 'La reseña debe ser texto plano.', 'Error'))

    if errores:
        raise ValueError({"errors": errores}, 400)

    return body

def validar_id_parada(id_str: str) -> int:
    """Valida que el id de la parada recibido en la URL sea un entero válido y mayor a cero."""
    id_parada = validar_entero(id_str)
    return validar_minimo(id_parada, MIN_ID, 'id_parada')

def validar_relato(body: dict) -> dict:
    """Valida el cambio parcial del relato de una parada"""
    errores = []

    if not isinstance(body, dict):
        raise ValueError(
            {"errors": [construir_error(
                "invalid.body",
                "El body debe ser un objeto JSON.",
                "Formato incorrecto")]}, 400)

    contenido = body.get('relato_texto')
    if contenido is None:
        errores.append(construir_error(
            'missing.relato_texto',
            'El campo relato_texto es requerido.',
            'Requerido'))
    else:
        if not isinstance(contenido, list):
            errores.append(
                construir_error(
                    'invalid.format',
                    'El relato_texto debe ser una lista.',
                    'Formato incorrecto'))
        else:
            for bloque in contenido:
                if not isinstance(bloque, dict):
                    errores.append(construir_error(
                        'invalid.block', 
                        'El bloque debe ser un diccionario.',
                        'Estructura inválida'))
                elif not isinstance(bloque.get('tipo'), str) or not isinstance(bloque.get('datos'), dict):
                    errores.append(construir_error(
                        'invalid.block', 
                        'El tipo debe ser texto y los datos un objeto.',
                        'Estructura inválida'))

    if errores:
        raise ValueError({"errors": errores}, 400)

    return body

def validar_ciudad(body: dict) -> dict:
    """Valida el cambio parcial de la ciudad de una parada de forma directa"""
    
    if not isinstance(body, dict):
        raise ValueError({"errors": [construir_error(
            "invalid.body", "El body debe ser un objeto JSON.", "Formato incorrecto"
        )]}, 400)

    id_ciudad = body.get('id_ciudad')
    
    if id_ciudad is None:
        raise ValueError({"errors": [construir_error(
            'missing.id_ciudad', 'El campo id_ciudad es requerido.', 'Requerido'
        )]}, 400)

    if type(id_ciudad) is not int or id_ciudad <= 0:
        raise ValueError({"errors": [construir_error(
            'invalid.id_ciudad', 'El id_ciudad debe ser entero positivo.', 'Requerido'
        )]}, 400)

    return body

def validar_edicion_parada(body: dict) -> dict:
    """Valida la edición unificada de una parada desde el editor web."""
    if not isinstance(body, dict):
        raise ValueError({"errors": [construir_error("invalid.body", "El body debe ser JSON.", "Error")]}, 400)

    errores = []

    id_ciudad = body.get('id_ciudad')
    if type(id_ciudad) is not int or id_ciudad <= 0:
        errores.append(construir_error('invalid.id_ciudad', 'El id_ciudad debe ser entero positivo.', 'Requerido'))

    texto_resena = body.get('texto_resena')
    if texto_resena is not None and not isinstance(texto_resena, str):
        errores.append(construir_error('invalid.texto', 'La reseña debe ser texto plano.', 'Formato incorrecto'))

    if errores:
        raise ValueError({"errors": errores}, 400)

    return body