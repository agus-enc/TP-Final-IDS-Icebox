from flask import Flask
from routes.admin import admin_bp
from routes.imanes import imanes_bp
from routes.lugares import lugares_bp
from routes.usuarios import usuarios_bp
from routes.viajes import viajes_bp
from routes.imagenes import imagenes_bp
from routes.paradas import paradas_bp

app = Flask(__name__, static_folder='icebox/static', static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # Limita las subidas a 10 MB máximo

app.register_blueprint(admin_bp, url_prefix='/icebox')
app.register_blueprint(imagenes_bp, url_prefix='/icebox')
app.register_blueprint(imanes_bp, url_prefix='/icebox')
app.register_blueprint(lugares_bp, url_prefix='/icebox')
app.register_blueprint(usuarios_bp, url_prefix='/icebox')
app.register_blueprint(viajes_bp, url_prefix='/icebox')
app.register_blueprint(paradas_bp, url_prefix='/icebox')

if __name__ == '__main__':
    app.run(debug=True)