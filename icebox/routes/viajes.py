from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..services.viajes import crear_viaje, eliminar_viaje, eliminar_parada
from ..validators.viajes import validar_id_viaje, validar_id_parada
from ..utils import construir_error

viajes_bp = Blueprint("viajes", __name__)

@viajes_bp.route("/<int:id_usuario>/viajes", methods=["POST"])
def post_viaje(id_usuario):
    try:
        id_usuario = validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    body = request.get_json(silent=True)

    try:
        viaje_dto = crear_viaje(body, id_usuario)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]), status

    return jsonify(viaje_dto), 201

viajes_bp = Blueprint('viajes', __name__)

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

viajes_bp = Blueprint('viajes', __name__)

@paradas_bp.route('/paradas/<id_parada>', methods=['DELETE'])
def delete_parada(id_parada):
    try:
        id_parada_validada = validar_id_parada(id_parada)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    eliminado = eliminar_parada(id_parada_validada)

    if not eliminado:
        return jsonify(construir_error(
            code="PARADA_NOT_FOUND",
            message='Parada no encontrada',
            description=f"No existe una parada con id '{id_parada_validada}'"
        )), 404

    return '', 204