from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..services.viajes import crear_viaje

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