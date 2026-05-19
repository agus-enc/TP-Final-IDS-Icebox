from ..utils import construir_error

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
        errores.append(
            construir_error(
                'invalid.imagen_url',
                'La url de la imagen debe ser texto.',
                'Formato incorrecto'))

    contenido = body.get('relato_texto')
    if contenido is not None:
        if not isinstance(contenido, list):
            errores.append(
                construir_error(
                    'invalid.format',
                    'El relato_texto debe ser una lista.',
                    'Formato incorrecto'))
        else:
            for bloque in contenido:
                if not isinstance(bloque, dict):
                    errores.append(construir_error('invalid.block', 'El bloque debe ser un diccionario.',
                                                   'Estructura inválida'))
                    break
                if not isinstance(bloque.get('tipo'), str) or not isinstance(bloque.get('datos'), dict):
                    errores.append(construir_error('invalid.block', 'El tipo debe ser texto y los datos un objeto.',
                                                   'Estructura inválida'))
                    break

    if errores:
        raise ValueError({"errors": errores}, 400)

    return body