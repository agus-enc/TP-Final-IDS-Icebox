from flask import Blueprint, request, jsonify
from ..services.imagenes import agregar_imagen_viaje
from ..validators.imagenes import validar_datos_imagen_viaje
from ..services.imagenes import eliminar_portada_viaje
from ..dao.imagenes import obtener_imagenes_viaje_db
from ..utils import construir_error

imagenes_bp = Blueprint("imagenes", __name__)

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes", methods=["POST"])
def post_imagen_viaje(id_viaje_str):
    try:
        tipo_raw = request.form.get('tipo', 'diario')
        archivo_imagen = request.files.get('imagen')

        datos_limpios = validar_datos_imagen_viaje(id_viaje_str, tipo_raw)

        if not archivo_imagen:
            raise ValueError({"errors": [{"code": "missing.file", "message": "No se envió imagen."}]}, 400)

        archivo_imagen.seek(0, 2)
        if archivo_imagen.tell() > 10485760:  # 10 MB
            raise ValueError({"errors": [{"code": "file_too_large", "message": "Supera 10MB."}]}, 413)
        archivo_imagen.seek(0)

        resultado = agregar_imagen_viaje(
            datos_limpios['id_viaje'],
            datos_limpios['tipo'],
            archivo_imagen
        )

        return jsonify(resultado), 201

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes", methods=["GET"])
def get_imagenes_viaje(id_viaje_str):
    try:
        id_viaje = int(id_viaje_str)
        imagenes = obtener_imagenes_viaje_db(id_viaje)
        return jsonify(imagenes), 200
    except ValueError:
        return jsonify({"errors": [{"code": "invalid", "message": "ID Invalido"}]}), 400

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes/header", methods=["DELETE"])
def delete_portada(id_viaje_str):
    try:
        id_viaje = int(id_viaje_str)
        eliminar_portada_viaje(id_viaje)
        return '', 204
    except ValueError:
        return jsonify({"errors": [{"message": "ID Inválido"}]}), 400