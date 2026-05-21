from mysql.connector import connect
from contextlib import contextmanager

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
    sql = "SELECT * FROM usuarios WHERE id_usuario = %(id_usuario)s"
    resultados = ejecutar_consulta(sql, {"id_usuario" : id_usuario})

    return resultados[0] if resultados else None

def eliminar_usuario_por_id(id_usuario: int) -> bool:
    """
    Elimina un usuario por id. Retorna True si fue eliminado, False si no existía
    """
    usuario = obtener_usuario(id_usuario)
    if not usuario:
        return False
    
    sql = "DELETE FROM usuarios WHERE id_usuario = %(id_usuario)s"
    ejecutar_mutacion(sql, {"id_usuario" : id_usuario})

def eliminar_parada_por_id(id_parada: int) -> bool:
    """Elimina un parada por id. Retorna True si existía y fue eliminado, False si no existía."""
    sql_buscar = 'SELECT 1 FROM paradas WHERE id_parada = %(id_parada)s'
    existe_parada = ejecutar_consulta(sql_buscar, {"id_parada": id_parada})

    if not existe_parada:
        return False
    sql_borrar = 'DELETE FROM paradas WHERE id_parada = %(id_parada)s'
    ejecutar_mutacion(sql_borrar, {'id_parada': id_parada})
    return True

def actualizar_posicion_iman(id_iman: int, ubicacion_heladera: bool, posicion_x: float, posicion_y: float) -> bool:
    """
    Guarda la posición final del imán, y si está o no en la heladera (booleano)
    """
    sql = """
        UPDATE imanes
        SET ubicación_heladera = %(ubicacion_heladera)s,
            posicion_x = %(posicion_x)s,
            posicion_y = %(posicion_y)s
        WHERE id_iman = %(id_iman)s
    """
    filas_afectadas = ejecutar_mutacion(sql, {
        "id_iman": id_iman,
        "ubicacion_heladera": ubicacion_heladera,
        "posicion_x": posicion_x,
        "posicion_y": posicion_y
    })
    return filas_afectadas > 0

def obtener_usuario_por_viaje(id_viaje: int) -> int | None:
    sql = 'SELECT id_usuario FROM viajes WHERE id_viaje = %(id_viaje)s'
    resultados = ejecutar_consulta(sql, {'id_viaje': id_viaje})
    return resultados[0]['id_usuario'] if resultados else None

def obtener_ciudad_por_id(id_ciudad: int) -> int | None:
    sql = 'SELECT id_ciudad FROM ciudades WHERE id_ciudad = %(id_ciudad)s'
    resultados = ejecutar_consulta(sql, {'id_ciudad': id_ciudad})
    return resultados[0]['id_ciudad'] if resultados else None

def insertar_parada_con_iman(id_viaje: int, id_usuario: int, id_ciudad: int, orden_en_ruta: int, relato_str: str | None, imagen_url: str | None, predeterminado: bool) -> dict:
    with obtener_transaccion() as cursor:
        sql_parada = '''
                     INSERT INTO paradas (id_viaje, id_ciudad, orden_en_ruta, relato_texto)
                     VALUES (%(id_viaje)s, %(id_ciudad)s, %(orden_en_ruta)s, %(relato_texto)s)
                     '''
        cursor.execute(sql_parada, {
            "id_viaje": id_viaje, "id_ciudad": id_ciudad,
            "orden_en_ruta": orden_en_ruta, "relato_texto": relato_str
        })
        id_parada = cursor.lastrowid

        sql_iman = '''
                   INSERT INTO imanes (id_usuario, id_ciudad, id_parada, imagen_url, predeterminado)
                   VALUES (%(id_usuario)s, %(id_ciudad)s, %(id_parada)s, %(imagen_url)s, %(predeterminado)s)
                   '''
        cursor.execute(sql_iman, {
            "id_usuario": id_usuario, "id_ciudad": id_ciudad,
            "id_parada": id_parada,
            "imagen_url": imagen_url, "predeterminado": predeterminado
        })
        id_iman = cursor.lastrowid

        return {"id_parada": id_parada, "id_iman": id_iman}

def insertar_usuario(nombre_usuario: str, email: str, password: str)-> int:
    """
    Inserta un nuevo usuario y devuelve el id generado
    """
    sql = """
        INSERT INTO usuarios (nombre_usuario, email, password)
        VALUES (%(nombre_usuario)s, %(email)s, %(password)s)
        """
        
    return ejecutar_mutacion(sql, {"nombre_usuario": nombre_usuario, "email": email, "password": password})

def obtener_usuario_por_email(email: str)-> dict | None:
    """Busca un usuario por su mail (util para el login)"""
    
    sql = "SELECT * FROM usuarios WHERE email = %(email)s"
    resultados = ejecutar_consulta(sql, {"email": email})
    return resultados[0] if resultados else None

def actualizar_nombre_usuario(id_usuario: int, nombre_usuario: str)-> bool:
    """Actualiza el nombre de usuario"""
    
    sql = "UPDATE usuarios SET nombre_usuario = %(nombre_usuario)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "nombre_usuario": nombre_usuario})

    return filas_afectadas > 0

def actualizar_mail_usuario(id_usuario: int, email: str)-> bool:
    """Actualiza el correo electronico"""
    
    sql = "UPDATE usuarios SET email = %(email)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "email": email})

    return filas_afectadas > 0

def actualizar_password_usuario(id_usuario: int, password: str)-> bool:
    """Actualiza la contraseña del usuario"""
    
    sql = "UPDATE usuarios SET password = %(password)s WHERE id_usuario = %(id_usuario)s"
    filas_afectadas = ejecutar_mutacion(sql, {"id_usuario": id_usuario, "password": password})

    return filas_afectadas > 0

def obtener_imanes_usuario(id_usuario: int, en_heladera: bool) -> list:
    """
    Trae los imanes del usuario filtrados por su ubicación (heladera = True, cajón = False)
    """
    
    sql = """
        SELECT id_iman, id_usuario, imanes.id_ciudad, imanes.id_parada, paradas.id_viaje, imagen_url, predeterminado, ubicación_heladera, posicion_x, posicion_y
        FROM imanes
        INNER JOIN paradas
        ON imanes.id_parada = paradas.id_parada
        WHERE id_usuario = %(id_usuario)s
            AND ubicación_heladera = %(en_heladera)s
        """
    
    parametros = {
        "id_usuario": id_usuario,
        "en_heladera": en_heladera
    }

    resultado = ejecutar_consulta(sql, parametros)
    return resultado

def obtener_paises_por_usuario(id_usuario: int) -> list:
    sql = """
    SELECT DISTINCT p.id_pais, p.nombre
    FROM paises p
    JOIN ciudades c ON p.id_pais = c.id_pais
    JOIN paradas pa ON c.id_ciudad = pa.id_ciudad
    JOIN viajes v ON pa.id_viaje = v.id_viaje
    WHERE v.id_usuario = %(id_usuario)s;
    """

    return ejecutar_consulta(sql, {"id_usuario": id_usuario})