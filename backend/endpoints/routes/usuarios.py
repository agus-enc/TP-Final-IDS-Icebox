from flask import Blueprint, jsonify, request
from ..utils import construir_error
from ..validators.usuarios import validar_id_usuario, validar_registro_usuario, validar_login_usuario
from ..services.usuarios import eliminar_usuario, registrar_nuevo_usuario, autenticar_usuario, obtener_perfil_usuario, modificar_nombre, modificar_email, modificar_password

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios", methods=['POST'])
def registrar_usuario():
    data = request.get_json() or request.form.to_dict() or {}

    try:
        validar_registro_usuario(data)
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    
    nombre_usuario = data.get('nombre_usuario')
    email = data.get("email")
    password = data.get("password")
    
    try:
        nuevo_id = registrar_nuevo_usuario(nombre_usuario, email, password)
        return jsonify({"message": "Usuario registrado con exito", "id_usuario": nuevo_id}), 201
    
    except Exception as e:
        print("❌ ERROR REAL DEL BACKEND:", str(e))
        error_body = construir_error('database.error', 'Error al registrar', str(e))
        return jsonify(error_body), 400

@usuarios_bp.route("/usuarios/login", methods=['POST'])
def login():
    data = request.get_json() or {}
    
    try:
        validar_login_usuario(data)
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')
    
    usuario = autenticar_usuario(nombre_usuario, password)

    if not usuario:
        error_body = construir_error('invalid.credentials', 'Credenciales incorrectas', 'El email o la contraseña no coinciden')
        return jsonify(error_body), 401
    
    """Si coinciden, le devolvemos los datos del usuario (sin la password)"""
    usuario.pop('password', None)
    return jsonify({
        "message": "Autenticacion exitosa",
        "usuario": usuario,
    }), 200

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=['GET'])
def obtener_perfil(id_usuario):
    
    try:
        validar_id_usuario(id_usuario)

    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    
    usuario = obtener_perfil_usuario(id_usuario)
    if not usuario:
        error_body = construir_error('user.not_found', 'Usuario no encontrado', f'No existe un usuario con id {id_usuario}')
        return jsonify(error_body), 404
    
    usuario.pop('password', None)
    return jsonify(usuario), 200

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=['PATCH'])
def actualizar_perfil_usuario(id_usuario):
    try:
        validar_id_usuario(id_usuario)
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    
    id_buscado = int(id_usuario)

    data = request.get_json() or {}
    
    nuevo_nombre = data.get('nombre_usuario')
    nuevo_email = data.get('email')
    nueva_password = data.get('password')

    if not nuevo_nombre and not nuevo_email and not nueva_password:
        return jsonify({'message': 'No se proporcionaron campos para actualizar'}), 400

    # 1. Si vino nombre, intentamos modificarlo pero NO frenamos el código si falla
    if nuevo_nombre:
        modificar_nombre(id_buscado, nuevo_nombre)

    # 2. Si vino email, modificamos email
    if nuevo_email:
        try:
            actualizado = modificar_email(id_buscado, nuevo_email)
        except Exception as e:
            return jsonify({'message': 'El email ya esta en uso'}), 400

    # 3. Si vino password, modificamos password
    if nueva_password:
        actualizado = modificar_password(id_buscado, nueva_password)
        if not actualizado:
            return jsonify({'message': 'Usuario no encontrado para actualizar contraseña'}), 404
    
    return jsonify({'message': 'Datos de cuenta actualizados correctamente'}), 200


@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=["DELETE"])
def delete_usuario(id_usuario):
    
    try:
        id_usuario_validado = validar_id_usuario(id_usuario)
    except ValueError as e:
        error_dict = e.args[0]
        status = e.args[1] if len(e.args) > 1 else 400
        return jsonify(error_dict), status
    
    eliminado = eliminar_usuario(id_usuario_validado)

    if not eliminado:
        return jsonify(construir_error(
            code="USER NOT FOUND",
            message="Usuario no encontrado",
            description=f"No existe el usuario con id '{id_usuario_validado}'"
        )), 404
    
    return "", 204