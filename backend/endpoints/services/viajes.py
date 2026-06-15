from ..dao.viajes import insertar_viaje, eliminar_viaje_por_id, actualizar_titulo_viaje, obtener_viaje, obtener_viajes_por_usuario_db
from ..validators.viajes import validar_body_viaje, validar_id_viaje
from ..dao.imagenes import obtener_imagenes_viaje_db
from .imagenes import eliminar_portada_viaje, eliminar_imagen_diario
from ..dao.paradas import obtener_paradas_por_viaje
from ..dao.imanes import eliminar_iman_por_id
from .storage import borrar_imagen_supabase
import hashlib
SECRET_KEY = "icebox_ids"

def generar_firma_mapa(id_usuario):
    return hashlib.sha256(f"{id_usuario}{SECRET_KEY}".encode()).hexdigest()[:8]

def construir_viaje_dto(viaje: dict) -> dict:
    """ Construye el dict de respuesta básico de un viaje. """
    return {
        "id_viaje": viaje["id_viaje"],
        "id_usuario": viaje["id_usuario"],
        "titulo": viaje["titulo"],
    }

def obtener_viaje_por_id(id_viaje: int) -> dict:
    viaje = validar_id_viaje(id_viaje)
    return construir_viaje_dto(viaje)

def crear_viaje(body: dict, id_usuario: int) -> dict:
    """ Crea un nuevo viaje aplicando validaciones de DTO """
    datos_limpios = validar_body_viaje(body)

    nuevo_id = insertar_viaje(
        id_usuario=id_usuario,
        titulo=datos_limpios["titulo"]
    )

    return construir_viaje_dto({
        "id_viaje": nuevo_id,
        "id_usuario": id_usuario,
        "titulo": datos_limpios["titulo"]
    })

def eliminar_viaje(id_viaje: int) -> bool:
    """Elimina un viaje por id, limpiando previamente imágenes en Supabase y BD."""
    viaje = obtener_viaje(id_viaje)
    if not viaje:
        return False

    imagenes = obtener_imagenes_viaje_db(id_viaje)
    for img in imagenes:
        if img.get('tipo') == 'header':
            eliminar_portada_viaje(id_viaje)
        elif img.get('tipo') == 'diario':
            eliminar_imagen_diario(img['id_imagen'])

    paradas = obtener_paradas_por_viaje(id_viaje)
    for parada in paradas:
        id_iman = parada.get('id_iman')
        if id_iman:
            if not parada.get('predeterminado') and parada.get('imagen_url'):
                borrar_imagen_supabase(parada['imagen_url'])

            eliminar_iman_por_id(id_iman)

    return eliminar_viaje_por_id(id_viaje)

def obtener_todos_los_viajes() -> list:
    """Obtiene la lista completa de viajes desde la base de datos"""
    return "" # obtener_todos_los_viajes_db()

def editar_titulo_viaje(id_viaje: int, body: dict) -> bool:
    """Valida y actualiza el titulo de viaje existente"""
    datos_viaje = validar_body_viaje(body)
    titulo_limpio = datos_viaje.get("titulo")
    return actualizar_titulo_viaje(id_viaje, titulo_limpio)

def obtener_viajes_por_usuario(id_usuario: int) -> list:
    """Obtiene y formatea la lista de viajes de un usuario a formato dto"""
    lista = obtener_viajes_por_usuario_db(id_usuario)
    return [construir_viaje_dto(v) for v in lista]