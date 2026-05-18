from flask import Blueprint, jsonify, request
from ..utils import construir_error
from ..validators.usuarios import validar_id_usuario
from ..services.usuarios import eliminar_usuario

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def delete_usuario(id_usuario):
    
    try:
        id_usuario_validado = validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    eliminado = eliminar_usuario(id_usuario_validado)

    if not eliminado:
        return jsonify(construir_error(
            code="USER NOT FOUND",
            message="Usuario no encontrado",
            description=f"No existe el usuario con id '{id_usuario_validado}'"
        )), 404
    
    return "", 204