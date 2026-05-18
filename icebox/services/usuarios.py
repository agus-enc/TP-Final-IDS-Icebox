from .. import db

def eliminar_usuario(id_usuario: int) -> bool:
    """
    Elimina un usuario por id. Retorna True si fue eliminado, False si no existía
    """
    return db.eliminar_usuario_por_id(id_usuario)
