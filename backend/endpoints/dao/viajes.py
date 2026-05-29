from ..db import ejecutar_consulta, ejecutar_mutacion

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
    sql = 'DELETE FROM viajes WHERE id_viaje = %(id_viaje)s'
    filas_afectadas = ejecutar_mutacion(sql, {'id_viaje': id_viaje})
    return filas_afectadas > 0