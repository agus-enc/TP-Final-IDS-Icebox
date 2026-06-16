from flask import Blueprint, jsonify, request
from ..validators.usuarios import validar_id_usuario
from ..services.viajes import crear_viaje, eliminar_viaje, editar_titulo_viaje, obtener_viaje_por_id, obtener_viajes_por_usuario, generar_firma_mapa
from ..validators.viajes import validar_id_viaje
from ..utils import construir_error

viajes_bp = Blueprint("viajes", __name__)

@viajes_bp.route("/<int:id_usuario>/viajes", methods=["POST"])
def post_viaje(id_usuario):
    id_solicitante = request.headers.get('X-User-Id')
    if str(id_usuario) != str(id_solicitante):
        return jsonify({"errors": [{"message": "Acceso denegado. No puedes crear un viaje para otro usuario."}]}), 403
    try:
        id_usuario = validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    try:
        body = request.get_json(silent=True)
        if not body:
            raise ValueError({"errors": [{"code": "missing.body", "message": "Falta el body JSON."}]}, 400)
        viaje_dto = crear_viaje(body, id_usuario)

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

    return jsonify(viaje_dto), 201

@viajes_bp.route('/viajes/<int:id_viaje>', methods=['DELETE'])
def delete_viaje(id_viaje):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        viaje_existente = validar_id_viaje(id_viaje)
        if str(viaje_existente['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado. No puedes borrar este viaje."}]}), 403
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

    eliminado = eliminar_viaje(viaje_existente["id_viaje"])

    if not eliminado:
        return jsonify(construir_error(
            code="VIAJE_NOT_FOUND",
            message='Viaje no encontrado',
            description=f"No existe un viaje con id '{id_viaje}'"
        )), 404

    return '', 204

@viajes_bp.route("/viajes/<int:id_viaje>", methods=["GET"])
def get_viaje(id_viaje):
    try:
        viaje_dto = obtener_viaje_por_id(id_viaje)
        return jsonify(viaje_dto), 200
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

@viajes_bp.route('/viajes/<int:id_viaje>', methods=['PUT'])
def put_viaje(id_viaje):
    id_solicitante = request.headers.get('X-User-Id')
    try:
        viaje_existente = validar_id_viaje(id_viaje)
        if str(viaje_existente['id_usuario']) != str(id_solicitante):
            return jsonify({"errors": [{"message": "Acceso denegado."}]}), 403
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

    body = request.get_json(silent=True)

    try:
        editar_titulo_viaje(viaje_existente["id_viaje"], body)
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status

    return '', 204

@viajes_bp.route("/<int:id_usuario>/viajes/lista", methods=["GET"])
def get_viajes_usuario(id_usuario):
    try:
        validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400

    viajes = obtener_viajes_por_usuario(id_usuario) 
    
    return jsonify(viajes), 200

@viajes_bp.route("/<int:id_usuario>/validar-acceso", methods=["GET"])
def validar_acceso_mapa(id_usuario):
    id_solicitante = request.headers.get('X-User-Id')
    
    if str(id_usuario) == str(id_solicitante):
        return jsonify({"permitido": True, "token_compartir": generar_firma_mapa(id_usuario)}), 200
        
    token_recibido = request.args.get('token')
    token_correcto = generar_firma_mapa(id_usuario)
    
    if token_recibido == token_correcto:
        try:
            validar_id_usuario(id_usuario) 
            return jsonify({"permitido": True, "token_compartir": token_correcto}), 200
        except ValueError as e:
            return jsonify(e.args[0]), 400
            
    return jsonify({"errors": [{"message": "Acceso denegado. El enlace no es válido."}]}), 403