import requests
from flask import session
from constants import BACKEND_URL

def parsear_formulario_paradas(formulario, archivos):
    """
    Extrae y organiza todos los datos crudos del formulario HTML
    en una lista ordenada de diccionarios limpios.
    """
    paradas_data = []
    for key in formulario.keys():
        if key.startswith('texto_parada_'):
            indice = key.split('_')[-1]

            id_parada_str = formulario.get(f'id_parada_{indice}')
            id_parada = int(id_parada_str) if id_parada_str and id_parada_str.strip() else None

            id_ciudad_str = formulario.get(f'ciudad_parada_{indice}')
            id_ciudad = int(id_ciudad_str) if id_ciudad_str and id_ciudad_str.strip() else 0

            paradas_data.append({
                "indice": int(indice),
                "id_parada": id_parada,
                "id_ciudad": id_ciudad,
                "texto_resena": formulario.get(f'texto_parada_{indice}'),
                "tipo_iman": formulario.get(f'tipo_iman_{indice}'),
                "pais_iman": formulario.get(f'pais_iman_{indice}'),
                "archivo_iman": archivos.get(f'archivo_iman_{indice}')
            })

    # Ordenamos por índice para asegurar que se procesen en la ruta correcta
    paradas_data.sort(key=lambda x: x['indice'])
    return paradas_data

def procesar_paquete_iman(lote_imanes, archivos_imanes, id_parada, datos_parada):
    """
    Agrega el imán de una parada específica al lote maestro que viajará al backend.
    """
    tipo_iman = datos_parada.get('tipo_iman')
    indice = datos_parada.get('indice')

    if tipo_iman == 'ninguno':
        lote_imanes.append({"id_parada": id_parada, "tipo": "ninguno"})

    elif tipo_iman == 'predeterminado':
        lote_imanes.append({
            "id_parada": id_parada,
            "tipo": "predeterminado",
            "pais": datos_parada.get('pais_iman')
        })

    elif tipo_iman == 'personalizado':
        archivo = datos_parada.get('archivo_iman')
        if archivo and archivo.filename != '':
            archivo_key = f"file_{indice}"
            archivos_imanes[archivo_key] = (archivo.filename, archivo.read(), archivo.content_type)
            lote_imanes.append({
                "id_parada": id_parada,
                "tipo": "personalizado",
                "archivo_key": archivo_key
            })


def es_propietario_del_viaje(id_viaje):
    """Verifica si el viaje solicitado pertenece al usuario de la sesión actual"""
    if session.get('es_admin'):
        return True

    resp = requests.get(f"{BACKEND_URL}/viajes/{id_viaje}")
    if resp.status_code == 200:
        viaje = resp.json()
        return str(viaje.get('id_usuario')) == str(session.get('usuario_id'))

    return False