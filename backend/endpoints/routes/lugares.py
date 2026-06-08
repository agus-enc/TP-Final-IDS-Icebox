from flask import Blueprint, jsonify
from ..services.lugares import obtener_paises_visitados, obtener_paises, obtener_ciudades_por_pais, obtener_todas_las_ciudades
from ..utils import construir_error

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

@lugares_bp.route("/paises", methods=["GET"])
def get_paises():
    try:
        paises_dto = obtener_paises()
        return jsonify(paises_dto), 200
    except Exception:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudieron obtener los países",
            description="Ocurrio error interno al procesar la solicitud"
        )), 500

@lugares_bp.route("/paises/<int:id_pais>/ciudades", methods=["GET"])
def get_ciudades(id_pais):
    """Endpoint para obtener las ciudades de un país específico por su ID."""
    try:
        ciudades_list = obtener_ciudades_por_pais(id_pais)
        return jsonify(ciudades_list), 200
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    except Exception:
        return jsonify(construir_error(
            code="SERVER_ERROR",
            message="No se pudieron obtener las ciudades",
            description="Ocurri un error interno al procesar la solicitud."
        )), 500

@lugares_bp.route("/ciudades", methods=["GET"])
def get_todas_ciudades():
    try:
        ciudades_list = obtener_todas_las_ciudades()
        return jsonify(ciudades_list), 200
    except Exception:
        return jsonify({"error": "Error interno"}), 500