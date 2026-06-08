from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from auth import login_required
from constants import BACKEND_URL
import requests

imanes_bp = Blueprint('imanes', __name__)

@imanes_bp.route('/')
@imanes_bp.route('/heladera')
@login_required
def mostrar_heladera():
    usuario_id = session.get('usuario_id')
    
    imanes_heladera = []
    try:
        url_api = f"{BACKEND_URL}/imanes?ubicacion=heladera"
        #El id_usuario se pasa en el header
        headers = {'X-User-Id': str(usuario_id)}
        respuesta = requests.get(url_api, headers=headers)
        if respuesta.status_code == 200:
            imanes_heladera = respuesta.json()
    except Exception as e:
        flash("No se pudieron cargar los imanes de la heladera.", "error")

    return render_template('heladera.html', imanes=imanes_heladera, usuario_id=usuario_id)

@imanes_bp.route('/cajon')
@login_required
def cajon():
    usuario_id = session.get('usuario_id')
    
    imanes_cajon = []
    try:
        url_api = f"{BACKEND_URL}/imanes?ubicacion=cajon"
        #El id_usuario se pasa en el header
        headers = {'X-User-Id': str(usuario_id)}
        respuesta = requests.get(url_api, headers=headers)
        if respuesta.status_code == 200:
            imanes_cajon = respuesta.json()
    except Exception as e:
        flash("No se pudieron cargar los imanes del cajón.", "error")

    return render_template('cajon.html', imanes=imanes_cajon, usuario_id=usuario_id)