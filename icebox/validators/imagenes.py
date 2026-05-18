from ..utils import construir_error
from ..constants import EXTENSIONES_PERMITIDAS, MIME_TYPES_PERMITIDOS

def validar_imagen(archivo) -> None:
    """  Verifica el nombre y la extension del archivo """
    if archivo.filename == '':
        raise ValueError(construir_error(
            code='invalid.file',
            message='El archivo no tiene nombre.',
            description='Se requiere un archivo válido.'
        ), 400)

    if '.' not in archivo.filename:
        raise ValueError(construir_error(
            code='invalid.extension',
            message='El archivo no tiene extensión.',
            description='Formato desconocido.'
        ), 400)

    extension = archivo.filename.rsplit('.', 1)[1].lower()

    if extension not in EXTENSIONES_PERMITIDAS:
        raise ValueError(construir_error(
            code='invalid.extension',
            message=f'Extensión no permitida: {extension}',
            description=f'Formatos válidos: {EXTENSIONES_PERMITIDAS}'
        ), 400)

    if archivo.mimetype not in MIME_TYPES_PERMITIDOS:
        raise ValueError(construir_error(
            code='invalid.file_type',
            message=f'El archivo no es una imagen real',
            description=f'Formatos válidos: {EXTENSIONES_PERMITIDAS}'
        ), 400)