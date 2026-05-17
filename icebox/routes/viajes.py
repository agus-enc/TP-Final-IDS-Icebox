from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..utils import construir_error
from ..services.viajes import crear_viaje

viajes_bp = Blueprint("viajes", __name__)

@viajes_bp.route("/<id_usuario>/viajes", methods=["POST"])
def post_viaje(id_usuario):
    try:
        id_usuario = validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    body = request.get_json(silent=True)

    if body is None:
        return jsonify(construir_error(
            code=400,
            message='Cuerpo de la solicitud inválido',
            description='El cuerpo debe ser un JSON válido'
        )), 400

    try:
        crear_viaje(body, id_usuario)
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]), status

    return '', 201