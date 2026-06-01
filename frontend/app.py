from flask import Flask
from datetime import timedelta
import json
import urllib.request as cliente_http
from urllib.error import URLError, HTTPError
import requests
from constants import BACKEND_URL

from routes.login import login_bp
from routes.imanes import imanes_bp
from routes.viajes import viajes_bp
from routes.mapa import mapa_bp
from routes.admin import admin_bp

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'icebox_trips_secretkey'
app.permanent_session_lifetime = timedelta(hours=3)

@app.context_processor
def inyectar_ciudades_global():
    try:
        resp = requests.get(f"{BACKEND_URL}/ciudades")
        lugares = resp.json() if resp.status_code == 200 else []
    except:
        lugares = []
    return dict(lugares=lugares)

app.register_blueprint(login_bp)
app.register_blueprint(imanes_bp)
app.register_blueprint(viajes_bp)
app.register_blueprint(mapa_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000) 