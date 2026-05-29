from ..db import ejecutar_consulta, ejecutar_mutacion

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

def actualizar_posicion_iman(id_iman: int, ubicacion_heladera: bool, posicion_x: float, posicion_y: float) -> bool:
    """
    Guarda la posición final del imán, y si está o no en la heladera (booleano)
    """
    sql = """
          UPDATE imanes
          SET ubicación_heladera = %(ubicacion_heladera)s,
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
