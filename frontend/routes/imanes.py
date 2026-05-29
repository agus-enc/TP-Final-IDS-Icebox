from flask import Blueprint, render_template, session
from auth import login_required

imanes_bp = Blueprint('imanes', __name__)

@imanes_bp.route('/')
@imanes_bp.route('/heladera')
@login_required
def mostrar_heladera():
    usuario_id = session.get('usuario_id')
    imanes_heladera = []
    return render_template('heladera.html', imanes=imanes_heladera, usuario_id=usuario_id)

@imanes_bp.route('/cajon')
@login_required
def cajon():
    usuario_id = session.get('usuario_id')
    imanes_cajon = []
    return render_template('cajon.html', imanes=imanes_cajon, usuario_id=usuario_id)