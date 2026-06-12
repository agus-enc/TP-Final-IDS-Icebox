from flask import Blueprint, request, jsonify
from ..services.paradas import crear_parada, eliminar_parada, eliminar_relato, modificar_relato_parada, modificar_ciudad_parada, editar_parada_completa, obtener_paradas_de_viaje
from ..validators.paradas import  validar_id_parada
from ..validators.viajes import validar_id_viaje
from ..utils import construir_error

paradas_bp = Blueprint("paradas", __name__)

@paradas_bp.route("/viajes/<int:id_viaje>/paradas", methods=["POST"])
def post_parada(id_viaje):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        viaje_bd = validar_id_viaje(id_viaje)
        if str(viaje_bd['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado. Este viaje no te pertenece."}]}), 403
    except ValueError as e:
        return jsonify(e.args[0]), 400

    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)

        resultado_dto = crear_parada(id_viaje, body)
        return jsonify(resultado_dto), 201

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

@paradas_bp.route("/viajes/<int:id_viaje>/paradas", methods=["GET"])
def get_paradas_viaje(id_viaje):
    """Endpoint para obtener todas las paradas ordenadas de un viaje específico."""
    try:
        paradas = obtener_paradas_de_viaje(id_viaje)
        return jsonify(paradas), 200

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    except Exception as e:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudieron obtener las paradas.",
            description="Ocurrió un error interno en la base de datos."
        )), 500

@paradas_bp.route('/paradas/<int:id_parada>', methods=['DELETE'])
def delete_parada(id_parada):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        parada_validada = validar_id_parada(id_parada)
        viaje_bd = validar_id_viaje(str(parada_validada['id_viaje']))
        if str(viaje_bd['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado. Esta parada no es tuya."}]}), 403
    except ValueError as e:
        return jsonify(e.args[0]), 400

    id_parada_validada = parada_validada['id_parada']
    eliminado = eliminar_parada(id_parada_validada)

    if not eliminado:
        return jsonify(construir_error(
            code="PARADA_NOT_FOUND",
            message='Parada no encontrada',
            description=f"No existe una parada con id '{id_parada_validada}'"
        )), 404

    return '', 204

@paradas_bp.route('/paradas/<id_parada>/relato', methods=['DELETE'])
def delete_relato_parada(id_parada):
    try:
        parada_validada = validar_id_parada(id_parada)
        id_parada_validada = parada_validada['id_parada']
    except ValueError as e:
        return jsonify(e.args[0]), 400

    modificado = eliminar_relato(id_parada_validada)

    if not modificado:
        return jsonify(construir_error(
            code="PARADA_NOT_FOUND",
            message='Parada no encontrada',
            description=f"No existe una parada con id '{id_parada_validada}' para borrar su relato"
        )), 404

    return '', 204

@paradas_bp.route("/paradas/<int:id_parada>/relato", methods=["PATCH"])
def patch_relato(id_parada):
    """Endpoint para actualizar de forma parcial el relato de una parada."""
    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)
        resultado = modificar_relato_parada(id_parada, body)
        return jsonify(resultado), 200
        
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
        
    except Exception:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudo actualizar el relato de la parada.",
            description="Ocurrió un error interno en el servidor."
        )), 500

@paradas_bp.route("/paradas/<int:id_parada>/ciudad", methods=["PATCH"])
def patch_ciudad(id_parada):
    """Endpoint para actualizar de forma parcial la ciudad de una parada."""
    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)
        resultado = modificar_ciudad_parada(id_parada, body)
        return jsonify(resultado), 200
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    except Exception:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudo actualizar la ciudad de la parada.",
            description="Ocurrió un error interno en el servidor."
        )), 500

@paradas_bp.route("/paradas/<int:id_parada>", methods=["PUT"])
def put_parada(id_parada):
    """Endpoint unificado para actualizar ciudad y texto de una parada."""
    id_solicitante = request.headers.get('X-User-Id')
    try:
        parada_validada = validar_id_parada(id_parada)
        viaje_bd = validar_id_viaje(str(parada_validada['id_viaje']))
        if str(viaje_bd['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado. Esta parada no es tuya."}]}), 403
    except ValueError as e:
        return jsonify(e.args[0]), 400

    id_parada_validada = parada_validada['id_parada']

    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)

        editar_parada_completa(id_parada_validada, body)

        return '', 204

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status