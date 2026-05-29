from flask import Blueprint, render_template
from ..auth import login_required

viajes_bp = Blueprint('viajes', __name__)

@viajes_bp.route('/viaje/creador')
@login_required
def creador():
    return render_template('creador.html')

@viajes_bp.route('/biblioteca')
@login_required
def biblioteca():
    return render_template('biblioteca.html')

@viajes_bp.route('/editor')
def editor():
    return render_template('editor.html')

@viajes_bp.route('/map')
@login_required
def map():
    return render_template('map.html')