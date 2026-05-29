from ..dao.imanes import actualizar_posicion_iman, obtener_imanes_usuario, eliminar_iman_por_id

def modificar_posicion_iman(id_iman: int, ubicacion_heladera: bool, posicion_x: float, posicion_y: float) -> bool:
    return actualizar_posicion_iman(id_iman, ubicacion_heladera, posicion_x, posicion_y)

def listar_imanes(id_usuario: int, ubicacion_param: str = None) -> list:
    """
    Lógica para mapear los filtros de imanes
    Por defecto asume 'False' (vista de cajón)
    """

    if ubicacion_param == "heladera":
        en_heladera = True
    else:
        en_heladera = False
    
    return obtener_imanes_usuario(id_usuario, en_heladera)

def eliminar_iman(id_iman: int) -> bool:
    """Elimina un iman por id. Retorna True si existía y fue eliminado, False si no existía."""
    return eliminar_iman_por_id(id_iman)