from flask import Blueprint, jsonify
from ..services.lugares import obtener_paises_visitados

lugares_bp = Blueprint("lugares", __name__)

@lugares_bp.route("/usuarios/<int:id_usuario>/paises/visitados", methods=["GET"])
def get_paises_visitados(id_usuario):
    try:
        dto_paises_visitados = obtener_paises_visitados(id_usuario)
        return jsonify(dto_paises_visitados), 200
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status