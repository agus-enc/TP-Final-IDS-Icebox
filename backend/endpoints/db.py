from mysql.connector import connect
from contextlib import contextmanager
import os

def get_connection():
    return connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 3306)),
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

        sql_clean = sql.strip().upper()

        if sql_clean.startswith("INSERT"):
            return cursor.lastrowid or 0
        elif sql_clean.startswith(("UPDATE", "DELETE")):
            return cursor.rowcount or 0
        
        return 0

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@contextmanager
def obtener_transaccion():
    """
    Maneja el ciclo de vida de una transacción (Commit / Rollback automático) para querys complejas.
    Uso: with obtener_transaccion() as cursor: ...
    """
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        yield cursor # Le "presta" el cursor a la función que lo llame
        conexion.commit()
    except Exception as e:
        conexion.rollback() # Si en la función salta un error inesperado, revierte los cambios.
        raise e
    finally:
        cursor.close()
        conexion.close()