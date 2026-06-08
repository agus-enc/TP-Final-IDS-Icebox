from flask import Flask
from datetime import timedelta
from functools import lru_cache
from constants import BACKEND_URL
import requests

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

# Guarda las ciudades en cache para solo hacer la petición una vez
@lru_cache(maxsize=1)
def obtener_ciudades_cacheadas():
    try:
        resp = requests.get(f"{BACKEND_URL}/ciudades")
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error conectando al backend: {e}")
    return []

# Inyecta la variable en todos los templates
@app.context_processor
def inyectar_datos_globales_ssr():
    return dict(ciudades_db=obtener_ciudades_cacheadas())

app.register_blueprint(login_bp)
app.register_blueprint(imanes_bp)
app.register_blueprint(viajes_bp)
app.register_blueprint(mapa_bp)
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000) 