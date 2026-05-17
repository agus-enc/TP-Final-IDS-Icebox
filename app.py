from flask import Flask
from routes.admin import admin_bp
from routes.imanes import imanes_bp
from routes.lugares import lugares_bp
from routes.usuarios import usuarios_bp
from routes.viajes import viajes_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix='/icebox')
app.register_blueprint(imanes_bp, url_prefix='/icebox')
app.register_blueprint(lugares_bp, url_prefix='/icebox')
app.register_blueprint(usuarios_bp, url_prefix='/icebox')
app.register_blueprint(viajes_bp, url_prefix='/icebox')

if __name__ == '__main__':
    app.run(debug=True)