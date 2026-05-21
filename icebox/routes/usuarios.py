from flask import Blueprint, jsonify, request
from ..utils import construir_error
from ..validators.usuarios import validar_id_usuario, validar_registro_usuario, validar_login_usuario
from ..services.usuarios import eliminar_usuario, registrar_nuevo_usuario, autenticar_usuario, obtener_perfil_usuario, modificar_nombre, modificar_email, modificar_password

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios", methods=['POST'])
def registrar_usuario():
    data = request.get_json() or {}

    try:
        validar_registro_usuario(data)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    nombre_usuario = data.get('nombre_usuario')
    email = data.get("email")
    password = data.get("password")
    
    try:
        nuevo_id = registrar_nuevo_usuario(nombre_usuario, email, password)
        return jsonify({"message": "Usuario registrado con exito", "id_usuario": nuevo_id}), 201
    
    except Exception as e:
        error_body = construir_error('database.error', 'Error al registrar', str(e))
        return jsonify(error_body), 400

@usuarios_bp.route("/usuarios/login", methods=['POST'])
def login():
    data = request.get_json() or {}
    
    try:
        validar_login_usuario(data)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    email = data.get('email')
    password = data.get('password')
    
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

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=['GET'])
def obtener_perfil(id_usuario):
    
    try:
        validar_id_usuario(id_usuario)
    
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    usuario = obtener_perfil_usuario(id_usuario)
    if not usuario:
        error_body = construir_error('user.not_found', 'Usuario no encontrado', f'No existe un usuario con id {id_usuario}')
        return jsonify(error_body), 400
    
    usuario.pop('password', None)
    return jsonify(usuario), 200

@usuarios_bp.route("/usuarios/<int:id_usuario>", methods=['PATCH'])
def actualizar_nombre_usuario(id_usuario):

    try:
        validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    data = request.get_json() or {}
    nuevo_nombre = data.get('nombre_usuario')

    if not nuevo_nombre:
        error_body = construir_error('missing.field', 'Campo faltante', 'Debe proporcionar un nombre de usuario')
        return jsonify(error_body), 400
    
    nombre_actualizado = modificar_nombre(id_usuario, nuevo_nombre)

    if not nombre_actualizado:
        error_body = construir_error('user.not_found', 'No se pudo actualizar', 'El usuario no existe')
        return jsonify(error_body), 404
    
    return jsonify({'message': 'Datos de cuenta actualizados correctamente'}), 200

@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PATCH'])
def actualizar_email(id_usuario):

    try:
        validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    data = request.get_json() or {}
    nuevo_email = data.get('email')

    if not nuevo_email:
        error_body = construir_error('missing.fields', 'Campo faltante', 'Debe proporcionar un email')
        return jsonify(error_body), 400
    
    try:
        actualizado = modificar_email(id_usuario, nuevo_email)
        if not actualizado:
            error_body = construir_error('user.not_found', 'No se pudo actualizar el email', 'El usuario no existe')
            return jsonify(error_body), 404
        return jsonify({"message":"Dirección de correo electrónico modificada con exito"})
    except Exception as e:
        error_body = construir_error('database.error', 'El email ya esta en uso', str(e))
        return jsonify(error_body), 400
    
@usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PATCH'])
def actualizar_password(id_usuario):
     
    try:
        validar_id_usuario(id_usuario)
    except ValueError as e:
        return jsonify(e.args[0]), 400
    
    data = request.get_json() or {}
    nueva_password = data.get('password')

    if not nueva_password:
        error_body = construir_error('missing.field', 'Campo faltante', 'Debe proporcionar una password')
        return jsonify(error_body), 400
    
    actualizado = modificar_password(id_usuario, nueva_password)
    if not actualizado:
        error_body = construir_error('user.not_found', 'No se pudo actualzar', 'El usuario no existe')
        return jsonify(error_body), 404
    
    return jsonify({"message":"Contraseña modificada de forma segura"})
         
    


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