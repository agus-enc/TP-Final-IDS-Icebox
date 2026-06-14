from ..db import ejecutar_consulta

def obtener_estadisticas_viajes():
    """ Hace la consulta a la base de datos usando db.py para traer los destinos y cuantos viajes tiene cada uno """

    sql = """
        SELECT paises.nombre, COUNT(paradas.id_parada) AS cantidad
        FROM paradas
        INNER JOIN ciudades ON paradas.id_ciudad = ciudades.id_ciudad
        INNER JOIN paises ON ciudades.id_pais = paises.id_pais
        GROUP BY paises.id_pais, paises.nombre
        ORDER BY cantidad DESC
        LIMIT 5
    """
    resultados = ejecutar_consulta(sql, None)
    return resultados

def obtener_estadisticas_ubicacion_imanes():
    """Consulta a la base de datos los imanes ubicados en la heladera"""

    sql = """
        SELECT ubicacion_heladera, COUNT(*) as cantidad 
        FROM imanes 
        GROUP BY ubicacion_heladera
    """
    resultados = ejecutar_consulta(sql, None)
    return resultados

def obtener_estadisticas_reseñas_por_ciudad():
    """
    Trae las 5 ciudades que tienen más relatos/reseñas escritos en sus paradas.
    Retorna dos listas: ciudades y cantidades.
    """

    sql= """
        SELECT c.nombre AS ciudad, COUNT(p.id_parada) AS total_reseñas
        FROM paradas p
        JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        WHERE p.relato_texto IS NOT NULL AND p.relato_texto != ''
        GROUP BY c.id_ciudad, c.nombre
        ORDER BY total_reseñas DESC
        LIMIT 5;
    """
    resultado = ejecutar_consulta(sql, None)

    ciudades_reseñas = [fila['ciudad'] for fila in resultado]
    cant_reseñas = [fila['total_reseñas'] for fila in resultado]

    return ciudades_reseñas, cant_reseñas

def obtener_estadisticas_usuarios_mas_activos():
    """Consulta a la base de datos los usuarios con mas viajes creados"""

    sql= """
        SELECT u.nombre_usuario AS usuario, COUNT(v.id_viaje) AS total_viajes
        FROM usuarios u
        JOIN viajes v ON u.id_usuario = v.id_usuario
        GROUP BY u.id_usuario, u.nombre_usuario
        ORDER BY total_viajes DESC
        LIMIT 5;
    """
    resultado = ejecutar_consulta(sql, None)

    usuarios = [fila['usuario'] for fila in resultado]
    cant_viajes = [fila['total_viajes'] for fila in resultado]

    return usuarios, cant_viajes