import requests
from flask import Blueprint, render_template, session, redirect, url_for, flash, request as flask_request
from auth import login_required
from constants import BACKEND_URL

mapa_bp = Blueprint('mapa', __name__)

@mapa_bp.route('/mapa', defaults={'id_usuario': None})
@mapa_bp.route('/mapa/<int:id_usuario>')
@login_required
def mostrar_mapa(id_usuario=None):

    if id_usuario is None:
        id_usuario = session.get('usuario_id')
        if not id_usuario:
            return redirect(url_for('login.login'))
    
    id_logueado = session.get('usuario_id')
    headers = {'X-User-Id': str(id_logueado)}

    token_url = flask_request.args.get('token', '')
    url_permiso = f"{BACKEND_URL}/{id_usuario}/validar-acceso?token={token_url}"
    
    try:
        resp_permiso = requests.get(url_permiso, headers=headers)
        
        if resp_permiso.status_code != 200:
            flash("No tenés permiso para ver este mapa o el link es inválido.", "danger")
            return redirect(url_for('mapa.mostrar_mapa'))

        data_permiso = resp_permiso.json()
        token_mapa = data_permiso.get('token_compartir', '')
            
    except requests.exceptions.RequestException as e:
        print(f"Error al validar permisos: {e}")
        flash("Error de conexión con el servidor.", "danger")
        return redirect(url_for('mapa.mostrar_mapa'))

    id_usuario = session.get('usuario_id')
    url_backend = f"{BACKEND_URL}/usuarios/{id_usuario}/paises/visitados"

    paises_codigos = []
    try:
        response = requests.get(url_backend)
        if response.status_code == 200:
            json_completo = response.json()
            lista_de_paises = json_completo.get('paises', [])
            
            paises_codigos = [pais['codigo'] for pais in lista_de_paises if 'codigo' in pais]   
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con el backend de lugares: {e}")

    datos_imanes = {}
    for codigo in paises_codigos:
        url_imanes = f"{BACKEND_URL}/usuarios/{id_usuario}/paises/{codigo}/imanes"
        try:
            resp_imanes = requests.get(url_imanes)
            if resp_imanes.status_code == 200:
                lista_imanes_pais = resp_imanes.json()
                
                for iman in lista_imanes_pais:
                    id_iman = iman.get('id_iman')
                    url_resena = f"{BACKEND_URL}/imanes/{id_iman}/resena"
                    try:
                        resp_resena = requests.get(url_resena)

                        if resp_resena.status_code == 200:
                            data_resena = resp_resena.json()
                            iman['relato'] = data_resena.get('relato_texto', "Sin relato disponible.")
                        else:
                            iman['relato'] = "Sin relato disponible."
                    except Exception as e:
                        print(f" Error al traer reseña para imán {id_iman}: {e}")
                        iman['relato'] = "Sin relato disponible."
                
                datos_imanes[codigo] = lista_imanes_pais
            else:
                datos_imanes[codigo] = []
        except Exception as e:
            print(f" Error al traer imanes para {codigo}: {e}")
            datos_imanes[codigo] = []

    return render_template('map.html', 
                           paises_visitados=paises_codigos, 
                           datos_imanes=datos_imanes,
                           usuario_id=id_usuario,
                           token_mapa=token_mapa)

@mapa_bp.route('/mi-mapa')
@login_required
def mi_mapa():
    return redirect(url_for('mapa.mostrar_mapa', id_usuario=session.get('usuario_id')))
