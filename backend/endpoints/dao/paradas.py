from ..db import ejecutar_mutacion, obtener_transaccion

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

def eliminar_relato_parada_db(id_parada: int) -> bool:
    """Busca la parada y pone su columna relato_texto en NULL. Retorna True si se modificó, False si la parada no existía."""
    sql_vaciar = 'UPDATE paradas SET relato_texto = NULL WHERE id_parada = %(id_parada)s'
    filas_afectadas = ejecutar_mutacion(sql_vaciar, {'id_parada': id_parada})

    return filas_afectadas > 0

def eliminar_parada_por_id(id_parada: int) -> bool:
    """Elimina un parada por id. Retorna True si existía y fue eliminado, False si no existía."""
    sql_borrar = 'DELETE FROM paradas WHERE id_parada = %(id_parada)s'
    filas_afectadas = ejecutar_mutacion(sql_borrar, {'id_parada': id_parada})
    return filas_afectadas > 0

def actualizar_relato_parada_db(id_parada: int, relato_str: str) -> bool:
    """Actualiza la columna relato_texto de una parada específica. Retorna True si existía."""
    sql = 'UPDATE paradas SET relato_texto = %(relato_texto)s WHERE id_parada = %(id_parada)s'

    filas_afectadas = ejecutar_mutacion(sql, {
        'relato_texto': relato_str,
        'id_parada': id_parada
    })

    return filas_afectadas > 0

def actualizar_ciudad_parada_db(id_parada: int, id_ciudad: int) -> bool:
    """Actualiza la columna id_ciudad de una parada específica. Retorna True si existía."""
    sql = 'UPDATE paradas SET id_ciudad = %(id_ciudad)s WHERE id_parada = %(id_parada)s'

    filas_afectadas = ejecutar_mutacion(sql, {
        'id_ciudad': id_ciudad,
        'id_parada': id_parada
    })

    return filas_afectadas > 0