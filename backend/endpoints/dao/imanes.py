from ..db import ejecutar_consulta, ejecutar_mutacion

def obtener_iman_por_id(id_iman: int) -> dict | None:
    """Busca un imán por su ID y devuelve su diccionario (o None si no existe)"""

    sql = "SELECT id_iman, id_usuario, ubicacion_heladera, posicion_x, posicion_y FROM imanes WHERE id_iman = %(id_iman)s"

    resultados = ejecutar_consulta(sql, {'id_iman': id_iman})
    return resultados[0] if resultados else None

def obtener_imanes_usuario(id_usuario: int, en_heladera: bool) -> list:
    """
    Trae los imanes del usuario filtrados por su ubicación (heladera = True, cajón = False)
    """

    sql = """
        SELECT id_iman, id_usuario, imanes.id_ciudad, imanes.id_parada, paradas.id_viaje, imagen_url, predeterminado, ubicacion_heladera, posicion_x, posicion_y
        FROM imanes
        INNER JOIN paradas
        ON imanes.id_parada = paradas.id_parada
        WHERE id_usuario = %(id_usuario)s
            AND ubicacion_heladera = %(en_heladera)s
        """

    parametros = {
        "id_usuario": id_usuario,
        "en_heladera": en_heladera
    }

    resultado = ejecutar_consulta(sql, parametros)
    return resultado

def actualizar_posicion_iman(id_iman: int, ubicacion_heladera: bool, posicion_x: float, posicion_y: float) -> bool:
    """
    Guarda la posición final del imán, y si está o no en la heladera (booleano)
    """
    sql = """
          UPDATE imanes
          SET ubicacion_heladera = %(ubicacion_heladera)s,
              posicion_x         = %(posicion_x)s,
              posicion_y         = %(posicion_y)s
          WHERE id_iman = %(id_iman)s \
          """
    filas_afectadas = ejecutar_mutacion(sql, {
        "id_iman": id_iman,
        "ubicacion_heladera": ubicacion_heladera,
        "posicion_x": posicion_x,
        "posicion_y": posicion_y
    })
    return filas_afectadas > 0

def eliminar_iman_por_id(id_iman: int) -> bool:
    """Elimina un iman por id. Retorna True si existía y fue eliminado, False si no existía."""
    sql_borrar = 'DELETE FROM imanes WHERE id_iman = %(id_iman)s'
    filas_afectadas = ejecutar_mutacion(sql_borrar, {'id_iman': id_iman})

    return filas_afectadas > 0

def existe_iman_predeterminado_en_pais(id_viaje: int, pais: str, excluir_id_parada: int = 0) -> bool:
    """
    Verifica si en el viaje actual ya existe un imán 'predeterminado'
    asignado a este país (excluyendo la parada que estamos editando actualmente).
    """
    query = """
            SELECT 1
            FROM imanes i
                     JOIN paradas p ON i.id_parada = p.id_parada
                     JOIN ciudades c ON p.id_ciudad = c.id_ciudad
                     JOIN paises pa ON c.id_pais = pa.id_pais
            WHERE p.id_viaje = %(id_viaje)s
              AND pa.nombre = %(pais)s
              AND i.predeterminado = TRUE
              AND p.id_parada != %(excluir_id_parada)s
            LIMIT 1;
            """
    parametros = {
        "id_viaje": id_viaje,
        "pais": pais,
        "excluir_id_parada": excluir_id_parada
    }
    return len(ejecutar_consulta(query, parametros)) > 0

def crear_iman(id_parada: int, imagen_url: str, predeterminado: bool, posicion_x: int = 50, posicion_y: int = 50) -> int:
    """
    Inserta un nuevo imán deduciendo automáticamente el id_usuario e id_ciudad
    desde las tablas padre (paradas y viajes).
    """
    query = """
            INSERT INTO imanes (id_parada, id_usuario, id_ciudad, imagen_url, posicion_x, posicion_y, predeterminado)
            SELECT 
                %(id_parada)s, 
                v.id_usuario, 
                p.id_ciudad, 
                %(imagen_url)s, 
                %(posicion_x)s, 
                %(posicion_y)s, 
                %(predeterminado)s
            FROM paradas p
            INNER JOIN viajes v ON p.id_viaje = v.id_viaje
            WHERE p.id_parada = %(id_parada)s;
            """
    parametros = {
        "id_parada": id_parada,
        "imagen_url": imagen_url,
        "posicion_x": posicion_x,
        "posicion_y": posicion_y,
        "predeterminado": predeterminado
    }

    return ejecutar_mutacion(query, parametros)

def obtener_iman_por_parada(id_parada: int) -> dict | None:
    """Busca si la parada ya tiene un imán asignado para poder borrarlo."""
    sql = "SELECT id_iman, imagen_url, predeterminado FROM imanes WHERE id_parada = %(id_parada)s"
    resultados = ejecutar_consulta(sql, {'id_parada': id_parada})
    return resultados[0] if resultados else None

def eliminar_iman_por_parada(id_parada: int) -> bool:
    """Borra el registro del imán asociado a una parada específica."""
    sql = "DELETE FROM imanes WHERE id_parada = %(id_parada)s"
    return ejecutar_mutacion(sql, {'id_parada': id_parada}) > 0

def obtener_imanes_por_usuario_y_pais(id_usuario: int, codigo_pais: str) -> list:
    """ Obtiene los imanes que un usuario específico tiene en un país. """   
    sql = '''
        SELECT i.id_iman, i.imagen_url, c.nombre AS nombre_ciudad, p.nombre AS nombre_pais
        FROM imanes i
        JOIN ciudades c ON i.id_ciudad = c.id_ciudad
        JOIN paises p ON c.id_pais = p.id_pais
        WHERE i.id_usuario = %(id_usuario)s AND p.codigo = %(codigo_pais)s
    '''
    return ejecutar_consulta(sql, {"id_usuario": id_usuario, "codigo_pais": codigo_pais})

def obtener_relato_por_iman(id_iman: int) -> str | None:
    """Busca el relato_texto de la parada asociada a un imán específico."""
    sql = '''
        SELECT p.relato_texto 
        FROM paradas p
        JOIN imanes i ON p.id_parada = i.id_parada
        WHERE i.id_iman = %(id_iman)s
    '''
    resultado = ejecutar_consulta(sql, {"id_iman": id_iman})
    
    return resultado[0]['relato_texto'] if resultado else None