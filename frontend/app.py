from flask import Flask
from datetime import timedelta
import json
import urllib.request as cliente_http
from urllib.error import URLError, HTTPError

from routes.login import login_bp
from routes.imanes import imanes_bp
from routes.viajes import viajes_bp

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='/static')

app.secret_key = 'icebox_trips_secretkey'
app.permanent_session_lifetime = timedelta(hours=3)

app.register_blueprint(login_bp)
app.register_blueprint(imanes_bp)
app.register_blueprint(viajes_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000) 