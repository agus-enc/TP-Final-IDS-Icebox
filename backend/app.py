from flask import Flask
from endpoints.routes.imanes import imanes_bp
from endpoints.routes.lugares import lugares_bp
from endpoints.routes.usuarios import usuarios_bp
from endpoints.routes.viajes import viajes_bp
from endpoints.routes.imagenes import imagenes_bp
from endpoints.routes.paradas import paradas_bp
from endpoints.routes.admin import admin_bp

app = Flask(__name__, static_folder='endpoints/static', static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Limita las subidas a 10 MB máximo

app.register_blueprint(imagenes_bp, url_prefix='/endpoints')
app.register_blueprint(imanes_bp, url_prefix='/endpoints')
app.register_blueprint(lugares_bp, url_prefix='/endpoints')
app.register_blueprint(usuarios_bp, url_prefix='/endpoints')
app.register_blueprint(viajes_bp, url_prefix='/endpoints')
app.register_blueprint(paradas_bp, url_prefix='/endpoints')
app.register_blueprint(admin_bp, url_prefix=' /endpoints')

if __name__ == '__main__':
    app.run(debug=True)