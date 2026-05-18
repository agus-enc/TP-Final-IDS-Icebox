from flask import Blueprint, request, jsonify
from ..services.imagenes import subir_imagen
from ..utils import construir_error

imagenes_bp = Blueprint("imagenes", __name__)

@imagenes_bp.route("/imagenes", methods=["POST"])
def post_imagen():
    try:
        # Los archivos viajan en request.files
        if 'imagen' not in request.files:
            raise ValueError(construir_error(
                code="missing.file",
                message="No se encontró el campo 'imagen'.",
                description="La petición debe enviar el archivo usando form-data."
            ), 400)

        imagen = request.files['imagen']

        resultado_dto = subir_imagen(imagen)

        return jsonify(resultado_dto), 201

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status