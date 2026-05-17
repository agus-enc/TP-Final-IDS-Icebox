from mysql.connector import connect
from utils import construir_error

def get_connection():
    return connect(
        host="localhost",
        user="root",
        password="root",
        database="ICEBOX"
    )

def ejecutar_mutacion(sql: str, parametros: dict):
    """
        Ejecuta un INSERT, UPDATE o DELETE y hace commit.
        Retorna el id generado en caso de INSERT, o 0 en otro caso.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        resultado = cursor.execute(sql, parametros or {})

        conn.commit()

        return cursor.lastrowid or 0

    except Exception as error:
        raise ValueError(construir_error(500, "Internal Server Error", "Problema inesperado en el servidor"))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insertar_viaje(id_usuario, titulo, fecha):
    """Inserta un nuevo usuario y retorna el id generado."""

    sql = 'INSERT INTO viajes (id_usuario, titulo, fecha_viaje) VALUES (%(id_usuario)s, %(titulo)s, %(fecha_viaje)s)'

    return ejecutar_mutacion(sql, {"id_usuario": id_usuario, "titulo": titulo, "fecha_viaje": fecha})