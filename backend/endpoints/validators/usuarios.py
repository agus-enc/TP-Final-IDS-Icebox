from ..utils import construir_error, validar_minimo
from email_validator import validate_email, EmailNotValidError

def validar_id_usuario(id_usuario: int) -> int:
    id_usuario_int = int(id_usuario)
    return validar_minimo(id_usuario_int, 1, 'id')

def validar_registro_usuario(data: dict):
    """Valida los datos al crear un nuevo usuario"""
    nombre = data.get('nombre_usuario')
    email = data.get('email')
    password = data.get('password')

    if not nombre or not email or not password:
        raise ValueError(construir_error(
            code='invalid.fields',
            message='Campos obligatorios vacios',
            description='El nombre de usuario, email y contraseña no pueden estar vacios',
        ))

    try:
        validate_email(email)
    except EmailNotValidError as e:
            raise ValueError(construir_error(
                code='invalid.email',
                message='Formatos de email inválidos',
                description='El correo electrónico ingresado no tiene un formáto valido (ejemplo@dominio.com)'
            ))
            

    if len(password) < 4:
        raise ValueError(construir_error(
            code='invalid.password.length',
            message='Contraseña muy corta',
            description='La contraseña debe tener al menos 4 caracteres'
        ))

def validar_login_usuario(data: dict):
    """Valida que se ingresen las credenciales para el login"""
    nombre_usuario = data.get('nombre_usuario')
    password = data.get('password')

    if not nombre_usuario or not password:
        raise ValueError(construir_error(
            code='missing.credentials',
            message='Credenciales incompletas',
            description='Se requiere tanto el usuario como la contraseña para iniciar sesion'
        ))