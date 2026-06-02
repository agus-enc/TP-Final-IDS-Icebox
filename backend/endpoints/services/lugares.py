from ..dao.usuarios import obtener_usuario
from ..dao.lugares import obtener_paises_por_usuario, obtener_todos_los_paises_db, obtener_ciudad_por_id, obtener_todas_las_ciudades_db
from ..validators.usuarios import validar_id_usuario
from ..validators.lugares import validar_id_pais
from ..utils import construir_error

def obtener_paises_visitados(id_usuario: int) -> list:
    id_usuario = validar_id_usuario(id_usuario)

    usuario = obtener_usuario(id_usuario)
    if not usuario:
        raise ValueError({"errors": [
            construir_error(
                "not_found",
                "El usuario no existe.",
                "No se encontró el recurso solicitado.")]}, 404)

    resultados_db = obtener_paises_por_usuario(id_usuario)

    paises_list = [{"id_pais": f["id_pais"], "nombre": f["nombre"], "codigo": f["codigo"]} for f in resultados_db]

    return {
        "metadata": {
            "total_paises": len(paises_list),
            "id_usuario": id_usuario
        },
        "paises": paises_list
    }

def obtener_paises() -> list:
    resultados_db = obtener_todos_los_paises_db()

    paises_list = [{"id_pais": f["id_pais"], "nombre": f["nombre"]} for f in resultados_db]
    
    return paises_list

def obtener_ciudades_por_pais(id_pais: int) -> list:
    """Valida el ID del país y obtiene sus ciudades desde la base de datos."""
    id_pais_validado = validar_id_pais(id_pais)

    resultados_db = obtener_ciudad_por_id(id_pais_validado)
    
    return [{"id_ciudad": f["id_ciudad"], "nombre": f["nombre"]} for f in resultados_db]

def obtener_todas_las_ciudades() -> list:
    return obtener_todas_las_ciudades_db()