from flask import Blueprint, jsonify, request
from ..utils import construir_error
from ..validators.usuarios import validar_id_usuario, validar_registro_usuario, validar_login_usuario
from ..services.usuarios import eliminar_usuario, registrar_nuevo_usuario, autenticar_usuario, obtener_perfil_usuario, modificar_nombre, modificar_email, modificar_password

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios", methods=['POST'])
def registrar_usuario():
    data = request.get_json() or {}
    nombre_usuario = data.get('nombre_usuario')
    email = data.get("email")
    password = data.get("password")

    if not nombre_usuario or not email or not password:
        error_body = construir_error('missing_fields', 'Campos faltantes', 'nombre_usuario, email y password son requeridos para crear una cuenta')
        return jsonify(error_body), 400
    
    try:
        nuevo_id = registrar_nuevo_usuario(nombre_usuario, email, password)
        return jsonify({"message": "Usuario registrado con exito", "id_usuario": nuevo_id}), 201
    
    except Exception as e:
        error_body = construir_error('database.error', 'Error al registrar', str(e))
        return jsonify(error_body), 400


@usuarios_bp.route("/usuarios/login", methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        error_body = construir_error('missing.credentials', 'Faltan credenciales', 'Email y contraseña son requeridos para iniciar sesión')
        return jsonify(error_body), 400
    
    usuario = autenticar_usuario(email, password)

    if not usuario:
        error_body = construir_error('invalid.credentials', 'Credenciales incorrectas', 'El email o la contraseña no coinciden')
        return jsonify(error_body), 401
    
    """Si coinciden, le devolvemos los datos del usuario (sin la password)"""
    usuario.pop('password', None)
    return jsonify({
        "message": "Autenticacion exitosa",
        "usuario": usuario,
    }), 200

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