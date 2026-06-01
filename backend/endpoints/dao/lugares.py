from ..db import ejecutar_consulta

def obtener_ciudad_por_id(id_ciudad: int) -> int | None:
    sql = 'SELECT id_ciudad FROM ciudades WHERE id_ciudad = %(id_ciudad)s'
    resultados = ejecutar_consulta(sql, {'id_ciudad': id_ciudad})
    return resultados[0]['id_ciudad'] if resultados else None

def obtener_paises_por_usuario(id_usuario: int) -> list:
    sql = """
    SELECT DISTINCT p.id_pais, p.nombre, p.codigo
    FROM paises p
    JOIN ciudades c ON p.id_pais = c.id_pais
    JOIN paradas pa ON c.id_ciudad = pa.id_ciudad
    JOIN viajes v ON pa.id_viaje = v.id_viaje
    WHERE v.id_usuario = %(id_usuario)s;
    """

    return ejecutar_consulta(sql, {"id_usuario": id_usuario})

def obtener_todos_los_paises_db() -> list:
    """Trae todos los países de la tabla"""
    sql = "SELECT id_pais, nombre, continente FROM paises"
    resultados = ejecutar_consulta(sql, None)

    return resultados

def obtener_todas_las_ciudades_db() -> list:
    sql = '''
        SELECT c.id_ciudad, c.nombre, p.nombre as pais 
        FROM ciudades c
        JOIN paises p ON c.id_pais = p.id_pais
    '''
    return ejecutar_consulta(sql, None)