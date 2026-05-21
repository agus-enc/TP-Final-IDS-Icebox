from flask import Blueprint, request, jsonify
from ..services.paradas import crear_parada, eliminar_parada
from ..validators.paradas import  validar_id_parada
from ..utils import construir_error

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

@paradas_bp.route('/viajes/paradas/<int:id_parada>', methods=['DELETE'])
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