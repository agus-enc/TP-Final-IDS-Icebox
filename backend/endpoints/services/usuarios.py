from ..dao.usuarios import insertar_usuario, obtener_usuario_por_nombre, actualizar_nombre_usuario, actualizar_mail_usuario, actualizar_password_usuario

def registrar_nuevo_usuario(nombre_usuario: str, email: str, password: str) -> int:
    """ Llama a db.py para insertar en la tabla usuarios"""
    return insertar_usuario(nombre_usuario, email, password)

def autenticar_usuario(nombre_usuario: str, password: str) -> bool:

    usuario = obtener_usuario_por_nombre(nombre_usuario)
    if usuario:
        if usuario['password'] == password:
            return usuario
        return None

def modificar_nombre(id_usuario: int, nombre_usuario: str) -> bool:
    return actualizar_nombre_usuario(id_usuario, nombre_usuario)

def modificar_email(id_usuario: int, email: str) -> bool:
    return actualizar_mail_usuario(id_usuario, email)

def modificar_password(id_usuario: int, password: str) -> bool:
    return actualizar_password_usuario(id_usuario, password)
