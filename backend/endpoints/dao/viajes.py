from ..db import ejecutar_consulta, ejecutar_mutacion, get_connection

def insertar_viaje(id_usuario: int, titulo: str, fecha_viaje: str) -> int:
    """Inserta un nuevo viaje y retorna el id generado."""

    sql = 'INSERT INTO viajes (id_usuario, titulo, fecha_viaje) VALUES (%(id_usuario)s, %(titulo)s, %(fecha_viaje)s)'

    return ejecutar_mutacion(sql, {"id_usuario": id_usuario, "titulo": titulo, "fecha_viaje": fecha_viaje})

def obtener_viaje(id_viaje: int) -> dict | None:
    """Obtener un viaje especifico por id."""

    sql = 'SELECT * FROM viajes WHERE id_viaje = %(id_viaje)s'
    resultados = ejecutar_consulta(sql, {"id_viaje": id_viaje})

    return resultados[0] if resultados else None

def actualizar_titulo_viaje(id_viaje: int, titulo: str) -> bool:
    """Actualiza el título de un viaje. Retorna True si se modificó."""
    sql = 'UPDATE viajes SET titulo = %(titulo)s WHERE id_viaje = %(id_viaje)s'
    filas_afectadas = ejecutar_mutacion(sql, {"id_viaje": id_viaje, "titulo": titulo})
    return filas_afectadas > 0

def eliminar_viaje_por_id(id_viaje: int) -> bool:
    """Elimina un viaje por id. Retorna True si existía y fue eliminado, False si no existía."""
    sql = 'DELETE FROM viajes WHERE id_viaje = %(id_viaje)s'
    filas_afectadas = ejecutar_mutacion(sql, {'id_viaje': id_viaje})
    return filas_afectadas > 0

def obtener_viajes_por_usuario_db(id_usuario: int) -> list:
    """Obtiene todos los viajes de un usuario específico."""
    sql = 'SELECT id_viaje, id_usuario, titulo, fecha_viaje FROM viajes WHERE id_usuario = %(id_usuario)s'
    return ejecutar_consulta(sql, {"id_usuario": id_usuario})