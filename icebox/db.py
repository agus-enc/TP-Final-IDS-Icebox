from mysql.connector import connect

def get_connection():
    return connect(
        host="localhost",
        user="root",
        password="root",
        database="ICEBOX"
    )

def ejecutar_consulta(sql: str, parametros: dict) -> list:
    """
        Ejecuta un SELECT y devuelve todas las filas como lista de dicts.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, parametros or {})
        resultados = cursor.fetchall()
        return resultados

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def ejecutar_mutacion(sql: str, parametros: dict) -> int:
    """
        Ejecuta un INSERT, UPDATE o DELETE y hace commit.
        Retorna el id generado en caso de INSERT, o 0 en otro caso.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(sql, parametros or {})
        conn.commit()

        return cursor.lastrowid or 0

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insertar_viaje(id_usuario: int, titulo: str, fecha_viaje: str) -> int:
    """Inserta un nuevo viaje y retorna el id generado."""

    sql = 'INSERT INTO viajes (id_usuario, titulo, fecha_viaje) VALUES (%(id_usuario)s, %(titulo)s, %(fecha_viaje)s)'

    return ejecutar_mutacion(sql, {"id_usuario": id_usuario, "titulo": titulo, "fecha_viaje": fecha_viaje})

def obtener_viaje(id_viaje: int) -> dict | None:
    """Obtener un viaje especifico por id."""

    sql = 'SELECT * FROM viajes WHERE id_viaje = %(id_viaje)s'
    resultados = ejecutar_consulta(sql, {"id_viaje": id_viaje})

    return resultados[0] if resultados else None

def eliminar_viaje_por_id(id_viaje: int) -> bool:
    """Elimina un viaje por id. Retorna True si existía y fue eliminado, False si no existía."""
    viaje = obtener_viaje(id_viaje)
    if not viaje:
        return False

    sql = 'DELETE FROM viajes WHERE id_viaje = %(id_viaje)s'
    ejecutar_mutacion(sql, {'id_viaje': id_viaje})
    return True

def obtener_usuario(id_usuario: int) -> dict | None:
    """
    Obtener un usuario específico por id
    """
    sql = "SELECT * FROM usuarios WHERE id = %(id_usuario)s"
    resultados = ejecutar_consulta(sql, {"id_usuario" : id_usuario})

    return resultados[0] if resultados else None

def eliminar_usuario_por_id(id_usuario: int) -> bool:
    """
    Elimina un usuario por id. Retorna True si fue eliminado, False si no existía
    """
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        return False
    
    sql = "DELETE FROM usuarios WHERE id = %(id_usuario)s"
    ejecutar_mutacion(sql, {"id_usuario" : id_usuario})
    return True