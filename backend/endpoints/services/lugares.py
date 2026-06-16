from ..dao.usuarios import obtener_usuario
from ..dao.lugares import obtener_paises_por_usuario, obtener_todas_las_ciudades_db
from ..validators.usuarios import validar_id_usuario
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

def obtener_todas_las_ciudades() -> list:
    return obtener_todas_las_ciudades_db()