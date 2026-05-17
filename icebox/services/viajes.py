from .. import db

def crear_viaje(body: dict, id_usuario: int):
    datos = {
        "id_usuario": id_usuario,
        "titulo": body["titulo"],
        "fecha_viaje": body["fecha_viaje"]
    }

    return db.insertar_viaje(datos["id_usuario"], datos["titulo"], datos["fecha_viaje"])