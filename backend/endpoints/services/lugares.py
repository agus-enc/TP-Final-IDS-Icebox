from .. import db
from ..validators.usuarios import validar_id_usuario
from ..utils import construir_error

def obtener_paises_visitados(id_usuario: int) -> dict:
    id_usuario = validar_id_usuario(id_usuario)

    usuario = db.obtener_usuario(id_usuario)
    if not usuario:
        raise ValueError({"errors": [
            construir_error(
                "not_found",
                "El usuario no existe.",
                "No se encontró el recurso solicitado.")]}, 404)

    resultados_db = db.obtener_paises_por_usuario(id_usuario)

    paises_list = [{"id_pais": f["id_pais"], "nombre": f["nombre"]} for f in resultados_db]

    return {
        "metadata": {
            "total_paises": len(paises_list),
            "id_usuario": id_usuario
        },
        "paises": paises_list
    }

def obtener_paises() -> list:
    resultados_db = db.obtener_todos_los_paises_db()

    paises_list = [{"id_pais": f["id_pais"], "nombre": f["nombre"]} for f in resultados_db]
    
    return paises_list
