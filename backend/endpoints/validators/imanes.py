from ..utils import construir_error, validar_entero, validar_minimo
from ..dao.imanes import obtener_iman_por_id
from ..constants import MIN_ID
from ..validators.usuarios import validar_id_usuario

def validar_id_iman(id_str: str) -> dict:
    """Valida formato del ID y verifica que el imán exista en la BD"""
    
    try:
        id_iman = validar_entero(id_str)
        id_iman = validar_minimo(id_iman, MIN_ID, 'id_iman')
    except ValueError as e:
        raise e

    iman = obtener_iman_por_id(id_iman)
    if not iman:
        error = construir_error(
            code="NOT_FOUND", 
            message="El imán solicitado no existe.",
            description=f"No se encontró un imán con el ID {id_iman} en la base de datos."
        )
        raise ValueError({"errors": [error]}, 404)
        
    return iman

def validar_body_posicion_iman(body: dict) -> dict:
    """Valida que el JSON tenga todos los datos necesarios"""
    if not body:
        raise ValueError(construir_error(
            "invalid.body",
            "El cuerpo de la petición está vacío",
            "Se requiere un JSON con 'ubicacion_heladera', 'posicion_x' y 'posicion_y'"
        ), 400) 

    errores = []

    ubicacion_heladera = body.get("ubicacion_heladera")

    if ubicacion_heladera in (1, 0, "1", "0"):
        ubicacion_heladera = bool(int(ubicacion_heladera))

    if ubicacion_heladera is None or not isinstance(ubicacion_heladera, bool):
        errores.append(construir_error(
            code='invalid.ubicacion_heladera',
            message='Campo requerido o inválido: ubicacion_heladera.',
            description="La ubicación en la heladera es obligatoria y debe ser un booleano (true/false)."
        )['errors'][0])

    posicion_x = body.get("posicion_x")
    if posicion_x is None:
        errores.append(construir_error(
            code='invalid.posicion_x',
            message='Campo requerido: posicion_x.',
            description="La coordenada X es obligatoria."
        )['errors'][0])
    else:
        try:
            posicion_x = float(posicion_x)
        except (ValueError, TypeError):
            errores.append(construir_error(
                code='invalid.posicion_x_type',
                message='Tipo de dato inválido: posicion_x.',
                description="La coordenada X debe ser un número válido."
            )['errors'][0])

    posicion_y = body.get("posicion_y")
    if posicion_y is None:
        errores.append(construir_error(
            code='invalid.posicion_y',
            message='Campo requerido: posicion_y.',
            description="La coordenada Y es obligatoria."
        )['errors'][0])
    else:
        try:
            posicion_y = float(posicion_y)
        except (ValueError, TypeError):
            errores.append(construir_error(
                code='invalid.posicion_y_type',
                message='Tipo de dato inválido: posicion_y.',
                description="La coordenada Y debe ser un número válido."
            )['errors'][0])

    if errores:
        raise ValueError({"errors": errores}, 400)

    return {
        "ubicacion_heladera": ubicacion_heladera,
        "posicion_x": posicion_x,
        "posicion_y": posicion_y
    }

def validar_autorizacion_iman(id_usuario_header: str | None, id_iman_url: str) -> dict:
    """
    Centraliza TODA la seguridad de la ruta:
    - 401: Verifica si el usuario mandó la cabecera y si es válida.
    - 403: Verifica si el imán le pertenece al usuario.
    """

    if not id_usuario_header:
        error_401 = construir_error(
            code="UNAUTHORIZED",
            message="Falta identificacion de usuario.",
            description="La cabecera X-User-Id es obligatoria para realizar esta acción."
        )
        raise ValueError(error_401, 401)

    id_usuario_validado = validar_id_usuario(id_usuario_header)
    
    iman_existente = validar_id_iman(str(id_iman_url))
    
    if iman_existente["id_usuario"] != id_usuario_validado:
        error_403 = construir_error(
            code="FORBIDDEN",
            message="Acceso denegado.",
            description="No tenés permisos para modificar este imán porque no te pertenece."
        )
        raise ValueError({"errors": [error_403]}, 403)
        
    return iman_existente