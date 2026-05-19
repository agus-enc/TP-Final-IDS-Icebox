from flask import Blueprint, request, jsonify
from ..services.paradas import crear_parada

paradas_bp = Blueprint("paradas", __name__)

@paradas_bp.route("/viajes/<int:id_viaje>/paradas", methods=["POST"])
def post_parada(id_viaje):
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