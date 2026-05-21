import os

MIN_ID         = 1
EXTENSIONES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'webp'}
MIME_TYPES_PERMITIDOS = {'image/png', 'image/jpeg', 'image/webp'}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
STATIC_URL_PATH = '/static/uploads/'