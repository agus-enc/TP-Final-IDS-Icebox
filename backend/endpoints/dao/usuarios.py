from ..db import ejecutar_consulta, ejecutar_mutacion

def insertar_usuario(nombre_usuario: str, email: str, password: str) -> int:
    """
    Inserta un nuevo usuario y devuelve el id generado
    """
    sql = """
          INSERT INTO usuarios (nombre_usuario, email, password)
          VALUES (%(nombre_usuario)s, %(email)s, %(password)s) \
          """

    return ejecutar_mutacion(sql, {"nombre_usuario": nombre_usuario, "email": email, "password": password})

def obtener_usuario(id_usuario: int) -> dict | None:
    """
    Obtener un usuario específico por id
    """
    sql = "SELECT * FROM usuarios WHERE id_usuario = %(id_usuario)s"
    resultados = ejecutar_consulta(sql, {"id_usuario" : id_usuario})

    return resultados[0] if resultados else None

def obtener_usuario_por_nombre(nombre_usuario: str) -> dict | None:
    """Busca un usuario por su nombre de usuario (util para el login)"""
    sql = "SELECT * FROM usuarios WHERE nombre_usuario = %(nombre_usuario)s"
    resultados = ejecutar_consulta(sql, {"nombre_usuario": nombre_usuario})
    return resultados[0] if resultados else None

def obtener_usuario_por_viaje(id_viaje: int) -> int | None:
    """Consulta a la base de datos un usuario segun su id de viaje"""

    sql = 'SELECT id_usuario FROM viajes WHERE id_viaje = %(id_viaje)s'
    resultados = ejecutar_consulta(sql, {'id_viaje': id_viaje})
    return resultados[0]['id_usuario'] if resultados else None

def obtener_usuario_por_email(email: str) -> dict | None:
    """Busca un usuario por su mail (util para el login)"""

    sql = "SELECT * FROM usuarios WHERE email = %(email)s"
    resultados = ejecutar_consulta(sql, {"email": email})
    return resultados[0] if resultados else None

def actualizar_nombre_usuario(id_usuario: int, nombre_usuario: str) -> bool:
    """Actualiza el nombre de usuario"""

    sql = "UPDATE usuarios SET nombre_usuario = %(nombre_usuario)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "nombre_usuario": nombre_usuario})

    return filas_afectadas > 0

def actualizar_mail_usuario(id_usuario: int, email: str) -> bool:
    """Actualiza el correo electronico"""

    sql = "UPDATE usuarios SET email = %(email)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "email": email})

    return filas_afectadas > 0

def actualizar_password_usuario(id_usuario: int, password: str) -> bool:
    """Actualiza la contraseña del usuario"""

    sql = "UPDATE usuarios SET password = %(password)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "password": password})

    return filas_afectadas > 0
