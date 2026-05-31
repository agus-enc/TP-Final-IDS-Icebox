from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..services.viajes import crear_viaje, eliminar_viaje, obtener_todos_los_viajes, editar_titulo_viaje, obtener_viaje_por_id
from ..validators.viajes import validar_id_viaje
from ..utils import construir_error

viajes_bp = Blueprint("viajes", __name__)

@viajes_bp.route("/<int:id_usuario>/viajes", methods=["POST"])
def post_viaje(id_usuario):
    try:
        id_usuario = validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)
        viaje_dto = crear_viaje(body, id_usuario)

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

    return jsonify(viaje_dto), 201

@viajes_bp.route('/viajes/<int:id_viaje>', methods=['DELETE'])
def delete_viaje(id_viaje):
    try:
        id_viaje_validado = validar_id_viaje(id_viaje)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    eliminado = eliminar_viaje(id_viaje_validado)

    if not eliminado:
        return jsonify(construir_error(
            code="VIAJE_NOT_FOUND",
            message='Viaje no encontrado',
            description=f"No existe un viaje con id '{id_viaje_validado}'"
        )), 404

    return '', 204

@viajes_bp.route("/viajes", methods=["GET"])
def get_viajes():
    try:
        viajes_dto = obtener_todos_los_viajes()
    except Exception as e:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudieron obtener los viajes",
            description="Ocurrio error interno al procesar la solicitud."
        )), 500

    return jsonify(viajes_dto), 200

@viajes_bp.route("/viajes/<int:id_viaje>", methods=["GET"])
def get_viaje(id_viaje):
    try:
        viaje_dto = obtener_viaje_por_id(id_viaje)
        return jsonify(viaje_dto), 200
    except ValueError as e:
        return jsonify(e.args[0]), e.args[1]

@viajes_bp.route('/viajes/<int:id_viaje>', methods=['PUT'])
def put_viaje(id_viaje):
    try:
        id_viaje_validado = validar_id_viaje(id_viaje)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    body = request.get_json(silent=True)

    try:
        editar_titulo_viaje(id_viaje_validado, body)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    return '', 204 # 204 No Content es el estándar para un PUT exitoso sin devolver datos
