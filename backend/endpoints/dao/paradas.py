from ..db import ejecutar_mutacion, obtener_transaccion, ejecutar_consulta

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

def obtener_paradas_por_viaje(id_viaje: int) -> list:
    """
    Obtiene todas las paradas de un viaje en orden,
    incluyendo su país y su imán (si es que tiene uno).
    """
    sql = '''
        SELECT p.id_parada, p.id_viaje, p.id_ciudad, p.orden_en_ruta, p.relato_texto AS texto_resena,
               c.nombre AS nombre_ciudad,
               pais.nombre AS pais_ciudad,
               i.id_iman, i.imagen_url, i.predeterminado
        FROM paradas p
        JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        JOIN paises pais ON c.id_pais = pais.id_pais
        LEFT JOIN imanes i ON p.id_parada = i.id_parada
        WHERE p.id_viaje = %(id_viaje)s
        ORDER BY p.orden_en_ruta ASC
    '''
    return ejecutar_consulta(sql, {'id_viaje': id_viaje})

def obtener_parada(id_parada: int) -> dict | None:
    """
    Busca una parada específica por su ID. Retorna el diccionario con los datos si existe, o None si no existe.
    """
    sql = '''
          SELECT id_parada, id_viaje, id_ciudad, orden_en_ruta, relato_texto
          FROM paradas
          WHERE id_parada = %(id_parada)s \
          '''
    resultados = ejecutar_consulta(sql, {'id_parada': id_parada})
    return resultados[0] if resultados else None

def eliminar_parada_por_id(id_parada: int) -> bool:
    """Elimina un parada por id. Retorna True si existía y fue eliminado, False si no existía."""
    sql_borrar = 'DELETE FROM paradas WHERE id_parada = %(id_parada)s'
    filas_afectadas = ejecutar_mutacion(sql_borrar, {'id_parada': id_parada})
    return filas_afectadas > 0

def actualizar_parada_completa(id_parada: int, id_ciudad: int, texto_resena: str) -> bool:
    """Actualiza la ciudad y el texto de una parada al mismo tiempo."""
    sql = '''
        UPDATE paradas 
        SET id_ciudad = %(id_ciudad)s, relato_texto = %(texto_resena)s 
        WHERE id_parada = %(id_parada)s
    '''
    filas_afectadas = ejecutar_mutacion(sql, {
        'id_ciudad': id_ciudad,
        'texto_resena': texto_resena,
        'id_parada': id_parada
    })
    return filas_afectadas > 0