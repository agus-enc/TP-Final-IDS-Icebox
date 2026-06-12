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