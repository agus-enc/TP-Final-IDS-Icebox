from ..dao.imanes import actualizar_posicion_iman, obtener_imanes_usuario, eliminar_iman_por_id, existe_iman_predeterminado_en_pais, crear_iman, obtener_iman_por_parada, eliminar_iman_por_parada, obtener_imanes_por_usuario_y_pais, obtener_relato_por_iman
from .procesador_ia import procesar_iman_ia
from .storage import subir_archivo_supabase, borrar_imagen_supabase
from ..dao.paradas import obtener_paradas_por_viaje
from ..validators.imanes import validar_body_posicion_iman

def modificar_posicion_iman(id_iman: int, body: dict) -> bool:
    """Procesa la actualización de coordenadas validando la estructura del JSON."""
    datos_limpios = validar_body_posicion_iman(body)
    return actualizar_posicion_iman(
        id_iman,
        datos_limpios["ubicacion_heladera"],
        datos_limpios["posicion_x"],
        datos_limpios["posicion_y"]
    )

def listar_imanes(id_usuario: int, ubicacion_param: str = None) -> list:
    """
    Lógica para mapear los filtros de imanes
    Por defecto asume 'False' (vista de cajón)
    """
    en_heladera = (ubicacion_param == "heladera")
    return obtener_imanes_usuario(id_usuario, en_heladera)

def eliminar_iman(id_iman: int) -> bool:
    """Elimina un iman por id. Retorna True si existía y fue eliminado, False si no existía."""
    return eliminar_iman_por_id(id_iman)

def listar_imanes_por_pais(id_usuario: int, codigo_iso: str) -> list:
    """Obtiene todos los imanes de un país usando su código ISO (ej: 'ARG')."""
    return obtener_imanes_por_usuario_y_pais(id_usuario, codigo_iso)

def obtener_resena_iman(id_iman: int) -> str | None:
    """Busca el relato_texto de la parada asociada a un imán específico."""
    return obtener_relato_por_iman(id_iman)

def procesar_lote_imanes(id_viaje: int, lista_datos: list, archivos_dict: dict) -> list:
    """Valída la existencia y el tipo de los imanes, borra y/o crea imanes
    tanto en la BD como en Supabase según corresponda"""
    # Traemos las paradas de este viaje para deducir los países comparando con la BD
    paradas_db = obtener_paradas_por_viaje(id_viaje)
    mapa_paises = {p['id_parada']: p['pais_ciudad'] for p in paradas_db}

    # Validación
    paises_usados_en_lote = set()
    imanes_a_procesar = []

    for item in lista_datos:
        tipo = item.get('tipo')
        id_parada = item.get('id_parada')

        if tipo == 'ninguno' or not tipo:
            imanes_a_procesar.append({'id_parada': id_parada, 'tipo': 'ninguno'})
            continue

        if tipo == 'predeterminado':
            # Deducimos el país usando el diccionario que armamos en el paso 0
            pais = mapa_paises.get(id_parada)

            if not pais:
                raise ValueError({"errors": [
                    {"message": f"Error de sincronización: No se encontró el país de la parada {id_parada}."}]})

            if pais in paises_usados_en_lote:
                raise ValueError(
                    {"errors": [{"message": f"No puedes asignar el imán de {pais} a múltiples paradas a la vez."}]})

            if existe_iman_predeterminado_en_pais(id_viaje, pais, excluir_id_parada=id_parada):
                raise ValueError(
                    {"errors": [{"message": f"Ya has usado el imán oficial de {pais} anteriormente en este viaje."}]})

            paises_usados_en_lote.add(pais)
            item['pais'] = pais
            imanes_a_procesar.append(item)

        elif tipo == 'personalizado':
            archivo_key = item.get('archivo_key')
            if not archivo_key or archivo_key not in archivos_dict:
                raise ValueError({"errors": [{"message": f"No se recibió el archivo de imagen."}]})
            imanes_a_procesar.append(item)

    # Ejecución
    resultados = []

    for item in imanes_a_procesar:
        id_parada = item['id_parada']
        tipo = item['tipo']

        # Averiguamos si existía un imán anterior
        iman_viejo = obtener_iman_por_parada(id_parada)

        # Caso borrar imán
        if tipo == 'ninguno':
            if iman_viejo:
                if not iman_viejo['predeterminado']:
                    borrar_imagen_supabase(iman_viejo['imagen_url'])
                eliminar_iman_por_parada(id_parada)
            continue

        # Caso imán oficial
        if tipo == 'predeterminado':
            if iman_viejo:
                if not iman_viejo['predeterminado']:
                    borrar_imagen_supabase(iman_viejo['imagen_url'])
                eliminar_iman_por_parada(id_parada)

            pais = item['pais']
            url_estatica = f"/static/images/imanes/{pais.lower().replace(' ', '_')}.png"
            nuevo_id = crear_iman(id_parada, url_estatica, predeterminado=True)
            resultados.append({"id_iman": nuevo_id, "id_parada": id_parada, "url": url_estatica})

        # Caso iman nuevo
        elif tipo == 'personalizado':
            archivo = archivos_dict[item['archivo_key']]
            bytes_png = procesar_iman_ia(archivo)
            url_publica = subir_archivo_supabase(
                file_bytes=bytes_png, filename=f"parada_{id_parada}.png",
                content_type="image/png", subcarpeta=f"viaje_{id_viaje}", bucket_name="imanes"
            )

            try:
                # Aseguramos el imán nuevo primero
                nuevo_id = crear_iman(id_parada, url_publica, predeterminado=False)

                # Limpiamos el viejo usando su ID para no matar al nuevo
                if iman_viejo:
                    if not iman_viejo['predeterminado']:
                        borrar_imagen_supabase(iman_viejo['imagen_url'])
                    eliminar_iman(iman_viejo['id_iman'])

                resultados.append({"id_iman": nuevo_id, "id_parada": id_parada, "url": url_publica})

            except Exception:
                # Si falló guardar en BD, borramos el nuevo de Supabase y el viejo sigue a salvo
                borrar_imagen_supabase(url_publica)
                raise ValueError({"errors": [{"message": "Fallo en base de datos. Rollback ejecutado."}]})

    return resultados