from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..services.viajes import crear_viaje, eliminar_viaje
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

@viajes_bp.route('/viajes/<id_viaje>', methods=['DELETE'])
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