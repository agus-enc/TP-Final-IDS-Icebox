from ..db import ejecutar_consulta, ejecutar_mutacion

def contar_imagenes_viaje_por_tipo_db(id_viaje: int, tipo: str) -> int:
    """Cuenta cuántas imágenes tiene un viaje dividiéndolas por 'header' o 'diario'."""
    sql = 'SELECT COUNT(*) as total FROM imagenes WHERE id_viaje = %(id_viaje)s AND tipo = %(tipo)s'
    resultado = ejecutar_consulta(sql, {'id_viaje': id_viaje, 'tipo': tipo})
    return resultado[0]['total'] if resultado else 0

def insertar_imagen_viaje_db(id_usuario: int, id_viaje: int, imagen_url: str, tipo: str, orden: int = 0, epigrafe: str = "") -> bool:
    """Guarda la URL en la BD asociándola al viaje, al usuario y a su tipo."""
    sql = '''
        INSERT INTO imagenes (id_usuario, id_viaje, imagen_url, tipo, orden, epigrafe) 
        VALUES (%(id_usuario)s, %(id_viaje)s, %(imagen_url)s, %(tipo)s, %(orden)s, %(epigrafe)s)
    '''
    filas_afectadas = ejecutar_mutacion(sql, {
        'id_usuario': id_usuario,
        'id_viaje': id_viaje,
        'imagen_url': imagen_url,
        'tipo': tipo,
        'orden': orden,
        'epigrafe': epigrafe
    })
    return filas_afectadas > 0

def obtener_imagenes_viaje_db(id_viaje: int) -> list:
    """Trae todas las imágenes asociadas a un viaje"""
    sql = 'SELECT id_imagen, imagen_url, tipo, orden, epigrafe FROM imagenes WHERE id_viaje = %(id_viaje)s'
    return ejecutar_consulta(sql, {'id_viaje': id_viaje})

def actualizar_portada_viaje_db(id_viaje: int, nueva_url: str) -> bool:
    """Sobrescribe la portada vieja por la nueva en BD"""
    sql = "UPDATE imagenes SET imagen_url = %(nueva_url)s WHERE id_viaje = %(id_viaje)s AND tipo = 'header'"
    return ejecutar_mutacion(sql, {'id_viaje': id_viaje, 'nueva_url': nueva_url}) > 0

def eliminar_portada_viaje_db(id_viaje: int) -> bool:
    """Elimina la portada de un viaje en BD"""
    sql = "DELETE FROM imagenes WHERE id_viaje = %(id_viaje)s AND tipo = 'header'"
    return ejecutar_mutacion(sql, {'id_viaje': id_viaje}) > 0

def obtener_imagen_por_id_db(id_imagen: int) -> dict:
    """Trae la información de una imagen específica"""
    sql = "SELECT id_imagen, imagen_url, id_usuario FROM imagenes WHERE id_imagen = %(id_imagen)s"
    res = ejecutar_consulta(sql, {'id_imagen': id_imagen})
    return res[0] if res else None

def eliminar_imagen_por_id_db(id_imagen: int) -> bool:
    """Elimina una foto del diario por su ID"""
    sql = "DELETE FROM imagenes WHERE id_imagen = %(id_imagen)s AND tipo = 'diario'"
    return ejecutar_mutacion(sql, {'id_imagen': id_imagen}) > 0

def actualizar_datos_imagen_db(id_imagen: int, epigrafe: str) -> bool:
    sql = "UPDATE imagenes SET epigrafe = %(epigrafe)s WHERE id_imagen = %(id_imagen)s AND tipo = 'diario'"
    return ejecutar_mutacion(sql, {'id_imagen': id_imagen, 'epigrafe': epigrafe}) > 0