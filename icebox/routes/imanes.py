from flask import Blueprint, jsonify, request
from ..utils import construir_error
from ..services.imanes import modificar_posicion_iman

imanes_bp = Blueprint("imanes", __name__)

@imanes_bp.route("/imanes/<int:id_iman>/posicion", methods=["PATCH"])
def cambiar_posicion_iman(id_iman):

    datos = request.get_json()

    ubicacion_heladera = datos.get("ubicacion_heladera")
    posicion_x = datos.get("posicion_x")
    posicion_y = datos.get("posicion_y")

    if ubicacion_heladera is None or posicion_x is None or posicion_y is None:
        return jsonify(construir_error(
            code="BAD_REQUEST",
            message="Faltan datos del posicionamiento",
            description="Los parámetros ubicacion_heladera, posicion_x, posicion_y son obligatorios en el body"
        )), 400
    
    try:
        exito = modificar_posicion_iman(id_iman, ubicacion_heladera, posicion_x, posicion_y)

        if not exito:
            return jsonify(construir_error(
                code="NOT_FOUND",
                message="El imán solicitado no existe",
                description=f"No se encontró ningún imán con el id {id_iman}"
            )), 404
        
        return "", 204
    
    except Exception as e:
        return jsonify(construir_error(
            code="INTERNAL_ERROR",
            message="Error interno del servidor",
            description=str(e)
        )), 500