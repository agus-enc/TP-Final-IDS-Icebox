from flask import Blueprint, request, jsonify
from ..services.imagenes import agregar_imagen_viaje, eliminar_imagen_diario, eliminar_portada_viaje, actualizar_datos_imagen, obtener_imagenes_viaje
from ..validators.imagenes import validar_datos_imagen_viaje
from ..validators.viajes import validar_id_viaje
from ..dao.imagenes import obtener_imagen_por_id_db

imagenes_bp = Blueprint("imagenes", __name__)

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes", methods=["POST"])
def post_imagen_viaje(id_viaje_str):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        viaje_bd = validar_id_viaje(id_viaje_str)
        if str(viaje_bd['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado."}]}), 403
    except ValueError as e:
        return jsonify(e.args[0]), 400

    try:
        tipo_raw = request.form.get('tipo', 'diario')
        archivo_imagen = request.files.get('imagen')
        orden = int(request.form.get('orden', 0))
        epigrafe = request.form.get('epigrafe', '')

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
            archivo_imagen,
            orden,
            epigrafe,
        )

        return jsonify(resultado), 201

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes", methods=["GET"])
def get_imagenes_viaje(id_viaje_str):
    try:
        viaje = validar_id_viaje(id_viaje_str)
        imagenes = obtener_imagenes_viaje(viaje["id_viaje"])
        return jsonify(imagenes), 200
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]), status

@imagenes_bp.route("/viajes/<string:id_viaje_str>/imagenes/header", methods=["DELETE"])
def delete_portada(id_viaje_str):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        viaje = validar_id_viaje(id_viaje_str)
        if str(viaje['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado."}]}), 403
        eliminar_portada_viaje(viaje["id_viaje"])
        return '', 204
    except ValueError as e:
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(e.args[0]), status

@imagenes_bp.route("/imagenes/<int:id_imagen>", methods=["DELETE"])
def delete_imagen_diario(id_imagen):
    id_solicitante = request.headers.get('X-User-Id')
    imagen_bd = obtener_imagen_por_id_db(id_imagen)
    if not imagen_bd:
        return jsonify({"errors": [{"message": "Imagen no encontrada."}]}), 404

    if str(imagen_bd['id_usuario']) != str(id_solicitante):
        return jsonify({"errors": [{"message": "Acceso denegado. Esta imagen pertenece a otro usuario."}]}), 403

    try:
        if eliminar_imagen_diario(id_imagen):
            return '', 204
        return jsonify({"errors": [{"message": "No se pudo eliminar la imagen."}]}), 400
    except Exception:
        return jsonify({"errors": [{"message": "Error interno al eliminar imagen."}]}), 500

@imagenes_bp.route("/imagenes/<int:id_imagen>", methods=["PUT"])
def update_imagen(id_imagen):
    id_solicitante = request.headers.get('X-User-Id')
    imagen_bd = obtener_imagen_por_id_db(id_imagen)
    if not imagen_bd:
        return jsonify({"errors": [{"message": "Imagen no encontrada."}]}), 404

    if str(imagen_bd['id_usuario']) != str(id_solicitante):
        return jsonify({"errors": [{"message": "Acceso denegado. Esta imagen pertenece a otro usuario."}]}), 403

    data = request.json or {}
    epigrafe = data.get('epigrafe', '')

    if actualizar_datos_imagen(id_imagen, epigrafe):
        return jsonify({"message": "Actualizado correctamente"}), 200
    return jsonify({"errors": [{"message": "No se pudo actualizar."}]}), 400