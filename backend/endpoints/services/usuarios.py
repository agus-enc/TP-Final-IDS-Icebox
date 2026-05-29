from ..dao.usuarios import insertar_usuario, obtener_usuario_por_email, obtener_usuario, actualizar_nombre_usuario, actualizar_mail_usuario, actualizar_password_usuario, eliminar_usuario_por_id

def registrar_nuevo_usuario(nombre_usuario: str, email: str, password: str) -> int:
    """ Llama a db.py para insertar en la tabla usuarios"""
    return insertar_usuario(nombre_usuario, email, password)

def autenticar_usuario(email: str, password: str) -> bool:

    usuario = obtener_usuario_por_email(email)
    if usuario:
        if usuario['password'] == password:
            return usuario
        return None

def obtener_perfil_usuario(id_usuario: int) -> dict | None:
    """Llama a la funcion en el db para traer el usuario por ID"""
    return obtener_usuario(id_usuario)

def modificar_nombre(id_usuario: int, nombre_usuario: str) -> bool:
    return actualizar_nombre_usuario(id_usuario, nombre_usuario)

def modificar_email(id_usuario: int, email: str) -> bool:
    return actualizar_mail_usuario(id_usuario, email)

def modificar_password(id_usuario: int, password: str) -> bool:
    return actualizar_password_usuario(id_usuario, password)

def eliminar_usuario(id_usuario: int) -> bool:
    """
    Elimina un usuario por id. Retorna True si fue eliminado, False si no existía
    """
    return eliminar_usuario_por_id(id_usuario)